import boto3
from botocore.auth import SigV4Auth
from botocore.credentials import create_credential_resolver
from botocore.awsrequest import AWSRequest


class Boto3LowLevelClient:
    _service_name: str
    _boto3_session = None
    _client = None

    def __init__(
        self, service_name: str, region_name: str = None, profile_name: str = None
    ) -> None:
        """
        Args:
            service_name (str): AWSのサービス名
            region_name (str): リージョン名(Optional)
            profile_name (str): プロファイル名(Optional)
        """
        self._service_name = service_name
        self._boto3_session = boto3.Session(
            region_name=region_name, profile_name=profile_name
        )
        self._client = self._boto3_session.client(service_name)

    def create_request_parameter(self, method_name: str, method_parameter: dict):
        """
        boto3への要求情報を作成する

        例:
        boto3_client.get_caller_identity({
            ...関数に引き渡すパラメータ
        })

        この関数での描き方:
        client.create_request_parameter("GetCallerIdentity", {
            ...関数に引き渡すパラメータ
        })

        Args:
            method_name (str): 関数名
            method_parameter (dict): 関数に引き渡すパラメータ
        """
        # クライアントから関数の定義情報を参照する
        operation_model = self._client._service_model.operation_model(method_name)
        request_dict = self._client._serializer.serialize_to_request(
            method_parameter, operation_model
        )

        # 今の環境に設定されている認証情報を取得する
        resolver = create_credential_resolver(self._boto3_session._session)
        credentials = resolver.load_credentials()
        # リージョン名を取得する
        region_name = self._boto3_session.region_name

        # リクエストに対して署名する
        request = AWSRequest(
            method=request_dict["method"],
            url=f"https://{self._service_name}.{region_name}.amazonaws.com{request_dict['url_path']}",
            data=request_dict["body"],
            headers=request_dict["headers"],
        )
        SigV4Auth(
            credentials=credentials,
            service_name=self._service_name,
            region_name=region_name,
        ).add_auth(request)

        # ヘッダを辞書型に詰め直す
        headers = {}
        for kv in request.headers.__dict__["_headers"]:
            headers[kv[0]] = kv[1]

        return {
            "method": request.method,
            "url": request.url,
            "body": request.body.decode("utf-8"),
            "headers": headers,
        }
