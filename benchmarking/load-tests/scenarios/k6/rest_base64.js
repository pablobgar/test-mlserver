import { group, sleep, check } from 'k6';
import http from "k6/http";
import { SharedArray } from 'k6/data';

let MLSERVER_HOST = "localhost";
let MLSERVER_HTTP_PORT = "8080";
let MODEL_NAME = "helloworld";

let DATA_PATH = "./data/base64-data.json"

// Rest test without random inputs as payloads

// HELPERS FUNCTIONS

/**
 * Pass if res equal 200 status code
 * @param {object} res http.post or http.get
 */
function checkResponse(res) {
    check(res, {
        "is status 200": (r) => r.status === 200,
    });
}

const randomData = new SharedArray('payloads', function () {
    return JSON.parse(open(DATA_PATH)).payloads
});



/**
 * Used for making post request to the mlserver model endpoint
 * __ENV Variables declared o test-plan.yml if running in pass
 * If running locally use k6 -e
 */
export class RestClient {
    constructor() {
        this.restHost = `http://${MLSERVER_HOST}:${MLSERVER_HTTP_PORT}`;
    }

    loadModel(name) {
        const res = http.post(`${this.restHost}/v2/repository/models/${name}/load`);

        checkResponse(res);
        return res;
    }

    unloadModel(name) {
        const res = http.post(
        `${this.restHost}/v2/repository/models/${name}/unload`
        );

        checkResponse(res);
        return res;
    }

    infer(name, payload) {
        const headers = { "Content-Type": "application/json" };
        const res = http.post(
        `${this.restHost}/v2/models/${name}/infer`,
        payload,
        { headers }
        );

        checkResponse(res);
        return res;
    }
}


// CONSTS DECLARATIONS


const rest = new RestClient();
const modelName = MODEL_NAME;


// LOAD TESTING FUNCTIONS

/**
 * If necessary, load the model here
 * @returns Data needed in default step lifecycle
 */
export function setup() {
    return randomData;
}

/**
 * Infer load testing function
 * __ENVs declared on const options for rest
 * @param {object} data TestData json prepared in setup step
 */
export default function (data) {
    group('infer_endpoint', function() {

        rest.infer(modelName, JSON.stringify(randomData[Math.floor(Math.random() * randomData.length)]));

    });

    sleep(0.001);
}
