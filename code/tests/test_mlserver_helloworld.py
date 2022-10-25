import pytest
from mlserver import types
from mlserver.settings import ModelSettings

from scoringsample.helloworld_example import CustomModel_helloworld

# FIXTURES:
#
# Used as helpers to run the tests.


@pytest.fixture
async def model() -> CustomModel_helloworld:
    """
    Loading the model to make it available for the inference.
    """
    model_settings = ModelSettings.parse_obj(
        {
            "name": "helloworld",
            "implementation": "scoringsample.helloworld_example.CustomModel_helloworld",
            "parameters": {"version": "0.1.0"},
        }
    )
    model = CustomModel_helloworld(model_settings)
    await model.load()

    return model


@pytest.fixture
def inference_request(request) -> types.InferenceRequest:
    """
    Request passed to the model for the tests.
    """
    request = {
        "parameters": {"content_type": "str"},
        "inputs": [
            {"name": "helloworld", "shape": [1], "datatype": "BYTES", "data": [""]}
        ],
        "outputs": [
            {
                "name": "helloworld",
                "parameters": {
                    "content_type": "BYTES",
                    "headers": {"content_type": "str"},
                },
            }
        ],
    }
    return types.InferenceRequest.parse_obj(request)


# UNIT TESTS:
#
# Write your tests here.
# Should be marked as asyncio for the fixtures to work.


@pytest.mark.asyncio
async def test_predict(model: CustomModel_helloworld, inference_request):
    """
    Inference the model and check the output data.
    """
    assert model.ready
    response = await model.predict(inference_request)
    for output in response.outputs:
        assert output.name == "helloworld"
        assert output.shape[0] == 1
        assert output.datatype == "BYTES"
        assert output.data[0] == b"Hello World"
