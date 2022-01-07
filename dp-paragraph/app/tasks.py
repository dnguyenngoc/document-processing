import json
from celery import Celery
from init_broker import is_broker_running
from init_redis import is_backend_running

from settings import config
from mq_main import redis


from worker.ml.model import CompletedModel
from worker.ml.helpers import image_utils as ml_image_helper
from helpers import time as time_helper
from helpers.storage import create_path, upload_file_bytes
from settings import (celery_config, config)


if not is_backend_running(): exit()
if not is_broker_running(): exit()


app = Celery(celery_config.QUERY_NAME, broker=config.BROKER, backend=config.REDIS_BACKEND)

app.config_from_object('settings.celery_config')

# class DBTask(Task):
#     _session = None
#     def after_return(self, *args, **kwargs):
#         if self._session is not None:
#             self._session.remove()
#     @property
#     def session(self):
#         if self._session is None:
#             self._session = get_session()
#         return self._session

@app.task(bind=True, 
          name="{query}.{task_name}".format(
              query=celery_config.QUERY_NAME, 
              task_name=celery_config.ML_PARAGRAPH_TASK_NAME))
def free_form(self, 
              task_id: str, 
              data: bytes):
    
    data = json.loads(data) # load session data
    time = time_helper.now_utc()
    data['time']['start_paragraph'] = str(time_helper.now_utc().timestamp())
    string_time = time_helper.str_yyyy_mm_dd(time)
    try:
        detect = CompletedModel()
        image = ml_image_helper.read_image_from_path_to_numpy(data['upload_result']['path'])
        height, width = image.shape[0:2]
        det = detect.predict(image)
        dir_path = celery_config.ML_STORAGE_PARAGRAPH_PATH + string_time
        # create_path(dir_path)
        # create_path(dir_path + '/' + task_id)
        det_new = {}
        for j in range(len(det)):
            de = det[j]
            xmin, ymin, xmax, ymax = de['box']
            if ymin < 0: ymin = 0
            if xmin < 0: xmin = 0
            center_w = int(width/2)
            if (xmax-xmin)/2 + xmin < center_w: 
                xmax = center_w
                xmin = 10
            else: 
                xmin = center_w
                xmax = width-10
            # upload = image[ymin:ymax, xmin:xmax]
            # bytes_image = ml_image_helper.numpy_to_io_bytes(upload)
            # paragraph_path = dir_path + '/' + task_id  + "/paragraph_{}".format(str(j)) + celery_config.ML_IMAGE_TYPE
            # upload_file_bytes(bytes_image, paragraph_path)
            obj = {}
            # obj['path'] = paragraph_path
            obj['confidence_level'] = str(de['confidence_level'])
            obj['box'] = ",".join([str(xmin), str(ymin), str(xmax), str(ymax)])
            # obj['box'] = (xmin, ymin, xmax,ymax)
            
            det_new['paragraph_{}'.format(j)] = obj
        data['time']['end_paragraph'] = str(time_helper.now_utc().timestamp())
        data['status']['paragraph_status'] = "SUCCESS"
        if len(det_new) > 0:
            data['paragraph_result'] = det_new
        data_dump = json.dumps(data)
        redis.set(task_id, data_dump)
        
        # sent key to id card field
        app.send_task(
            name="{query}.{task_name}".format(query=celery_config.ML_FIELD_QUERY_NAME, task_name=celery_config.ML_FIELD_TASK_NAME),
            kwargs={
                'task_id': task_id,
                'data': data_dump,
            },
            queue=celery_config.ML_FIELD_QUERY_NAME
        )        
    except Exception as e:
        data['time']['end_paragraph'] = str(time_helper.now_utc().timestamp())
        data['status']['paragraph_status'] = "FAILED"
        data['status']['general_status'] = "FAILED"
        data['error'] = str(e)
        data_dump = json.dumps(data)
        redis.set(task_id, data_dump)