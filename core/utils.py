from .models import ApplicationAuditLog
import json


def create_application_audit_log(user:str, object_changed:str, object_type:str, old_value=None, new_value=None, message=None):
    if old_value is None:
        old_value = {}
    elif isinstance(old_value, dict):
        old_value = json.dumps(old_value)
    else:
        old_value = {}

    if new_value is None:
        new_value = {}
    elif isinstance(new_value, dict):
        # new_value = json.dumps(new_value)
        new_value=new_value
    else:
        new_value = {}

    try:
        new_log = ApplicationAuditLog(changed_by=user, object_changed=object_changed, object_type=object_type,
                                      old_value=old_value, new_value=new_value, message=message)
        new_log.save()
        return True
    except Exception as e:
        print(e)
        return False
