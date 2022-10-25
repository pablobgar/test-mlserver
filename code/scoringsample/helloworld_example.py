import logging
from mlserver import MLModel, types


class CustomModel_helloworld(MLModel):

    async def load(self) -> bool:
        # This method is invoked one time a the start of the service
        # Place here the code to load the ML model.
        # If the applicacion does not have a model leave it with the following lines

        logging.debug("LOAD MODEL")
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        # This method invoked with every request (REST and GRPC)
        # Place here the inference code

        return types.InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[
                types.ResponseOutput(
                    name=self.name,
                    shape=[1],
                    datatype="BYTES",
                    data=[b"Hello World"],
                    parameters=types.Parameters(content_type="str"),
                )
            ],
        )
