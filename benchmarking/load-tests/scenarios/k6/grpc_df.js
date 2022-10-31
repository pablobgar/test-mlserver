import { group, sleep, check } from 'k6';
import { Counter } from "k6/metrics";
import grpc from "k6/net/grpc";
import { SharedArray } from 'k6/data';

let MLSERVER_HOST = "localhost";
let MLSERVER_GRPC_PORT = "8081";

let DATA_PATH = "./data/grpc-data.json"

const grpcReqs = new Counter("grpc_reqs");

function checkResponse(res) {
    check(res, {
        "status is OK": (r) => r && r.status === grpc.StatusOK,
    });
}

const randomData = new SharedArray('payloads', function () {
    return JSON.parse(open(DATA_PATH)).payloads
});

/**
 * Using two protos; dataplane for infer and model_repository for loading the model
 * @param {*} grpcHost
 * @returns grpc client
 */
function getClient(grpcHost) {
    const client = new grpc.Client();

    client.load([], "proto/dataplane.proto");

    return client;
}


export class GrpcClient {
    constructor() {
        this.grpcHost = `${MLSERVER_HOST}:${MLSERVER_GRPC_PORT}`;
        this.client = getClient(this.grpcHost);

        // Client can't connect on the init context
        this.connected = false;
    }

    infer(payload) {
        if (!this.connected) {
            this.client.connect(this.grpcHost, { plaintext: true });
            this.connected = true;
        }

        const res = this.client.invoke(
        "inference.GRPCInferenceService/ModelInfer",
        payload,
        );
        checkResponse(res);
        grpcReqs.add(1);
    }

    close() {
        this.client.close();
    }
}

// LOAD TESTING FUNCTIONS
const grpcCli = new GrpcClient();

/**
 * Infer k6 load test
 */
export default function () {
    group('infer_endpoint', function() {
        grpcCli.infer(randomData[Math.floor(Math.random() * randomData.length)]);
    });

    sleep(0.001);
}
