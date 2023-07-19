from typing import Union
from fastapi import FastAPI

import argo_workflows
from argo_workflows.api import workflow_service_api, workflow_template_service_api
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_submit_request import \
    IoArgoprojWorkflowV1alpha1WorkflowSubmitRequest


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/template")
def submit_workflow(namespace: str="staging"):
    config = argo_workflows.Configuration(host = "https://argo-server.argo:2746")
    config.verify_ssl = False

    # client = argo_workflows.ApiClient(config)
    # template_service = workflow_template_service_api.WorkflowTemplateServiceApi(api_client=client)
    # workflow_yaml= template_service.list_workflow_templates(namespace=namespace)

                  
    return {"template": config}  
    
@app.get("/run-workflow")
def submit_workflow(namespace: str="staging", template_name: str="fibonacci"):
    config = argo_workflows.Configuration(host = "https://argo-server.argo:2746")
    config.verify_ssl = False

    client = argo_workflows.ApiClient(config)
    service = workflow_service_api.WorkflowServiceApi(api_client=client)
    template_service = workflow_template_service_api.WorkflowTemplateServiceApi(api_client=client)
    workflow_yaml= template_service.get_workflow_template(namespace=namespace, name=template_name)

    submit_result = service.submit_workflow(namespace="staging",
                                body=IoArgoprojWorkflowV1alpha1WorkflowSubmitRequest(resource_kind="WorkflowTemplate",
                                                                                    resource_name=template_name,
                                                                                    _check_type=False),
                                _check_return_type=False)    
    return {"workflow": submit_result}    

