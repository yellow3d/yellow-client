
from http import HTTPStatus
import json
import logging
import os
from typing import List, Optional

from yellow.client import AuthenticatedClient
from yellow.client.api.auth import auth_token_create
from yellow.client.client import Client
from yellow.client.cli.common import HOST_DEFAULT, HOST_ENVVAR, TOKEN_ENVVAR
from yellow.client.models.auth_token_request import AuthTokenRequest
from yellow.client.models.error_message import ErrorMessage
from yellow.client.types import Response


logger = logging.getLogger("yellow-client")


class YellowAuthenticator:
    
    def __init__(
        self, 
        token: Optional[str] = None, 
        username: Optional[str] = None,
        password: Optional[str] = None,
        host_url: Optional[str] = None
    ):  

        if host_url is None:
            if (h := os.getenv(HOST_ENVVAR)) is not None:
                # use a host url defined under an env variable 
                self.host_url = h        
                logger.info(f"Connect to host: {self.host_url} found under the env variable {HOST_ENVVAR}")
            else:
                # use a default host url
                self.host_url = HOST_DEFAULT
                logger.info(f"Connect to the default host: {self.host_url}")
        else:
            self.host_url = host_url
            logger.info(f"Connect to the provided host: {self.host_url}")
        
        self.token = None
        self.client = None
        
        if token is not None:
            self.__token_auth(token)
            logger.info(f"Authenticate using token {token}")
        elif username is not None and password is not None:
            self.__auth(username, password)
            logger.info(f"Authenticate using username and password")
        elif (t := os.getenv(TOKEN_ENVVAR)) is not None:
            self.__token_auth(t)
            logger.info(f"Authenticate using token {t} found under the env variable {TOKEN_ENVVAR}")
        else:
            raise ValueError("Provide the pair (username and password) or token to authenticate.")
                    
    @classmethod
    def auth_with_token(cls, token: str, host_url: Optional[str] = None):
        """Authentication using token.

        Args:
            token (str): Yellow token
            host_url (Optional[str], optional): Yellow Host URL. Defaults to None. If None, use a default host

        Returns:
            YellowAuthenticator: Yellow authentication client instance
        """
        return cls(token=token, host_url=host_url)
    
    @classmethod
    def auth_with_account(cls, username: str, password: str, host_url: Optional[str] = None):
        """Authentication using username and password.

        Args:
            username (str): Yellow username
            password (str): Yellow password
            host_url (Optional[str], optional): Yellow Host URL. Defaults to None. If None, use a default host

        Returns:
            YellowAuthenticator: Yellow authentication client instance
        """
        return cls(username=username, password=password, host_url=host_url)
        
    def __token_auth(self, token: str) -> AuthenticatedClient:
        self.client = AuthenticatedClient(base_url=self.host_url, token=token)
        self.token = token
        
        return self.client       
            
    def __auth(self, username: str, password: str) -> Optional[AuthenticatedClient]:
        request = AuthTokenRequest(username=username, password=password)
        with Client(base_url=self.host_url) as preauth_client:
            response: Response = auth_token_create.sync_detailed(client=preauth_client, body=request)
            # self.raise_satus_error(response)
            
        if response.parsed is not None:
            token = response.parsed.token
            logger.info(f"Get Yellow API token: {token}")
            
            self.client = self.__token_auth(token)

        else:
            errors = json.loads(response.content).get("non_field_errors")
            if errors is None:
                errors = ["Undefined error during authorization"]
            raise ValueError(" ".join(errors))
            
        return self.client
    
    def raise_satus_error(self, response: Response):
        """Check if response returned 200 and 201 status code. If not, raise an error.

        Args:
            response (Response): Response received form the Yellow API

        Raises:
            ConnectionError: Error returned by the Yellow API
        """
        
        # accept 200 and 201
        if response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED):
            return
        
        err_msg = ""
        if isinstance(response.parsed, ErrorMessage):
            err_msg_obj = response.parsed
            err_msg = err_msg_obj.detail
            for i, k in enumerate(err_msg_obj.additional_keys):
                err_msg += f"[{k}] {' '.join(err_msg_obj.additional_properties[k])}"
                if i < len(err_msg_obj.additional_keys) - 1:
                    err_msg += "; "

        if err_msg == "":
            try:
                err_msg = json.loads(response.content)["detail"]
            except (json.JSONDecodeError, KeyError):
                err_msg = response.content.decode()
            finally:
                if err_msg is None or err_msg == "":
                    err_msg = "Undefined error during connecting with the API."
        
        logger.error(f"Status code: {response.status_code}. {err_msg} Response: {response.parsed}")            
        raise ConnectionError(f"Status code: {response.status_code}. {err_msg}")