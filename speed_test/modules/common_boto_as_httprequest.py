import boto3
from botocore.auth import SigV4Auth
from botocore.credentials import create_credential_resolver
from botocore.awsrequest import prepare_request_dict, create_request_object
from botocore.model import OperationModel


class Boto3LowLevelClient:
    _service_name: str
    _credential_scope: str
    _boto3_session = None
    _client = None

    def __init__(
        self,
        service_name: str,
        credential_scope: str = None,
        region_name: str = None,
        profile_name: str = None,
    ) -> None:
        """
        Args:
            service_name (str): AWSのサービス名
            credential_scope (str): 権限を有効化するAWSのサービス名(Optional)、Bedrock-Runtimeなど、権限とサービスが異なる場合に指定する
            region_name (str): リージョン名(Optional)
            profile_name (str): プロファイル名(Optional)
        """

        boto3.setup_default_session(region_name=region_name)
        self._service_name = service_name
        if credential_scope is None:
            self._credential_scope = service_name
        else:
            self._credential_scope = credential_scope
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
        operation_model: OperationModel = self._client._service_model.operation_model(
            method_name
        )
        request_dict = self._client._serializer.serialize_to_request(
            method_parameter, operation_model
        )

        # 今の環境に設定されている認証情報を取得する
        resolver = create_credential_resolver(self._boto3_session._session)
        credentials = resolver.load_credentials()
        # リージョン名を取得する
        region_name = self._boto3_session.region_name
        # エンドポイントのurlを取得する
        endpoint_url = f"https://{self._service_name}.{region_name}.amazonaws.com"

        prepare_request_dict(
            request_dict,
            endpoint_url,
            {
                "client_region": region_name,
                "client_config": self._client.meta.config,
                "has_streaming_input": operation_model.has_streaming_input,
                "auth_type": operation_model.auth_type,
            },
            user_agent=self._client._user_agent_creator.to_string(),
        )

        # リクエストに対して署名する
        request = create_request_object(request_dict)
        SigV4Auth(
            credentials=credentials,
            service_name=self._credential_scope,
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
