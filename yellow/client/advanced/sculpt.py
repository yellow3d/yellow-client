import json
import logging
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from tqdm import tqdm

from yellow.client.advanced.auth import YellowAuthenticator
from yellow.client.api.sculpt import (sculpt_characters_archive_partial_update,
                                      sculpt_characters_cancel_partial_update,
                                      sculpt_characters_create,
                                      sculpt_characters_feedback_create,
                                      sculpt_characters_fetch_retrieve,
                                      sculpt_characters_list,
                                      sculpt_characters_status_retrieve)
from yellow.client.models import CharacterFeedbackRequest, CharacterSpecRequest
from yellow.client.models.gender_enum import GenderEnum
from yellow.client.models.sculpt_characters_fetch_retrieve_file_format import SculptCharactersFetchRetrieveFileFormat
from yellow.client.models.sculpt_characters_fetch_retrieve_rig_type import SculptCharactersFetchRetrieveRigType
from yellow.client.types import Response

logger = logging.getLogger("yellow-client")


FILENAME_PATTERN = re.compile(r'attachment; filename="([^"]+)"')


class YellowSculpt:
    
    def __init__(
        self, 
        auth: YellowAuthenticator
    ):
        self.auth = auth
        self.api_client = auth.client

    def get_assets(self, **kwargs) -> Iterable[Dict]:
        """Get list of the historical list of prompts and generations.

        Yields:
            Generator[Dict]: Description of generated assets
        """
        page = 1
        while True:
            response: Response = sculpt_characters_list.sync_detailed(
                client=self.api_client, page=page, **kwargs
            )
            self.auth.raise_satus_error(response)
            paginated_list = json.loads(response.content.decode())
            yield from paginated_list["results"]
            if not paginated_list["next"]:
                break
            page += 1

    def get_latest_k_assets(self, k: int = 10, **kwargs) -> Iterable[Dict]:
        """Get list of latest k historical prompts and generations.

        Args:
            k (int): Numer of latest generations to return.

        Returns:
            List[Dict]: List of k latest descriptions of generated assets
        """
        response: Response = sculpt_characters_list.sync_detailed(
            client=self.api_client, page=1, page_size=k, **kwargs
        )
        self.auth.raise_satus_error(response)
        paginated_list = json.loads(response.content.decode())
        return paginated_list["results"]

    def get_assets_list(self, **kwargs) -> List[Dict]:
        """Get list of the historical list of prompts and generations.

        Returns:
            List[Dict]: List of descriptions of generated assets
        """
        return list(self.get_assets(**kwargs))

    def print_assets_list(self):
        """Print list of the historical list of prompts and generations.
        """
        assets_list = self.get_assets()
        for asset in assets_list:
            print(asset)
            
    def generate_asset(self, prompt: str, gender: str = "neutral") -> str:
        """Submit a new asset generation job. 

        Args:
            prompt (str): Prompt describing an asset
            gender (str, optional): Gender (male, female or netural). Defaults to "neutral"

        Raises:
            ValueError: Error recevied from the Yellow API during submitting a job

        Returns:
            str: UUID of a new asset
        """
        
        # select from {GenderEnum.MALE, GenderEnum.FEMALE, GenderEnum.NEUTRAL}
        # Note that you can specify gender using the attribute,
        # which can be helpful in reducing gender bias in some cases,
        # e.g. describing a profession, such as "a doctor".
        try:
            gender_enum = GenderEnum(gender)
        except ValueError:
            raise ValueError(f"Select gender from the list: {', '.join(enum.value for enum in GenderEnum)}")


        request = CharacterSpecRequest(prompt, gender_enum)
        response: Response = sculpt_characters_create.sync_detailed(client=self.api_client, body=request)
        self.auth.raise_satus_error(response)
        
        json_response = json.loads(response.content.decode())
        return json_response['uuid']
    
    
    def track_asset_generation(self, uuid: str, refresh_time: int = 2) -> Dict:
        """Track an asset generation process. Method uses tqdm to print a progress bar.  

        Args:
            uuid (str): UUID of an asset
            refresh_time (int, optional): Refresh time in seconds. Defaults to 2.

        Raises:
            ValueError: Error recevied from the Yellow API during checkign a job status

        Returns:
            Dict: Last generation job status
        """
        completed = False
        with tqdm(total=1, position=0, leave=True, desc="Status: _") as pbar:
            pbar.update(0)

            while not completed:
                response: Response = sculpt_characters_status_retrieve.sync_detailed(
                    client=self.api_client, generation_id=uuid,
                )
                self.auth.raise_satus_error(response)
                
                json_respone = json.loads(response.content.decode())
                if not 'state' in json_respone:
                    raise ValueError(f"Not found data for UUID: {uuid}")

                pbar.update(json_respone['progress']-pbar.n)
                pbar.set_description(f"Status: {json_respone['state']}")
                pbar.refresh() # to show immediately the update
                if json_respone['state'] == 'completed':
                    completed = True

                time.sleep(refresh_time)

            return json_respone        
        
    def add_feedback(self, uuid: str, feedback: str) -> Dict:
        """Add feedback for an asset.

        Args:
            uuid (str): UUID of an asset
            
        Raises:
            ConnectionError: Error recevied from the Yellow API during checkign a job status

        Returns:
            Dict: Feedback
        """
        logger.info(f"Adding feedback for UUID: {uuid}")
        request = CharacterFeedbackRequest(feedback, uuid)
        response: Response = sculpt_characters_feedback_create.sync_detailed(
            client=self.api_client, body=request,
        )
        self.auth.raise_satus_error(response)
        
        status_data = json.loads(response.content.decode())
        return status_data

    def cancel_generation(self, uuid: str) -> Dict:
        """Cancel an asset generation process.

        Args:
            uuid (str): UUID of an asset
            
        Raises:
            ConnectionError: Error recevied from the Yellow API during checkign a job status

        Returns:
            Dict: Cancellation status
        """
        logger.info(f"Canceling UUID: {uuid}")
        response: Response = sculpt_characters_cancel_partial_update.sync_detailed(
            client=self.api_client, 
            generation_id=uuid,
        )
        self.auth.raise_satus_error(response)
        
        status_data = json.loads(response.content.decode())
        return status_data

    def archive_generation(self, uuid: str) -> Dict:
        """Archive a generation.

        Args:
            uuid (str): UUID of an asset

        Raises:
            ConnectionError: Error recevied from the Yellow API during checking a job status

        Returns:
            Dict: UUID of an asset
        """
        logger.info(f"Archiving UUID: {uuid}")
        response: Response = sculpt_characters_archive_partial_update.sync_detailed(
            client=self.api_client, 
            generation_id=uuid,
        )
        self.auth.raise_satus_error(response)

        status_data = json.loads(response.content.decode())
        return status_data

    def check_asset_status(self, uuid: str) -> Dict:
        """Check current status of an asset generation process.

        Args:
            uuid (str): UUID of an asset
            
        Raises:
            ConnectionError: Error recevied from the Yellow API during checkign a job status

        Returns:
            Dict: Generation job status
        """
        logger.info(f"Checking status of UUID: {uuid}")
        response: Response = sculpt_characters_status_retrieve.sync_detailed(
            client=self.api_client, 
            generation_id=uuid,
        )
        self.auth.raise_satus_error(response)
        
        status_data = json.loads(response.content.decode())
        return status_data     
    
    def fetch_asset(
            self, 
            uuid: str, 
            output_dir: str, 
            file_format: str = SculptCharactersFetchRetrieveFileFormat.OBJ,
            rig_type: str = SculptCharactersFetchRetrieveRigType.NO_RIG,
        )-> str:
        """Fetch/download an generated asset.

        Args:
            uuid (str): UUID of an asset
            output_dir (str): Directory to store an asset
            file_format (str): File format of an asset
            rig_type (str): Rig type applied to a mesh

        Raises:
            ValueError: Error recevied from the Yellow API during fetching an asset

        Returns:
            str: Output path
        """

        file_format = SculptCharactersFetchRetrieveFileFormat(file_format)
        rig_type = SculptCharactersFetchRetrieveRigType(rig_type)

        logger.info(f"Checking status of UUID: {uuid}")
        response: Response = sculpt_characters_status_retrieve.sync_detailed(
            client=self.api_client, 
            generation_id=uuid,
        )
        self.auth.raise_satus_error(response)
    
        status_data = json.loads(response.content.decode())

        if status_data.get('state') == 'completed':
            logger.info(f"Fetching the asset of UUID: {uuid}")

            response: Response = sculpt_characters_fetch_retrieve.sync_detailed(
                client=self.api_client, 
                generation_id=uuid,
                file_format=file_format,
                rig_type=rig_type,
            )
            self.auth.raise_satus_error(response)

            if response.status_code == 200:
                if match := FILENAME_PATTERN.match(response.headers["content-disposition"]):
                    filename = match.group(1)

                output_dir = Path(output_dir)
                if not output_dir.exists():
                    output_dir.mkdir(parents=True, exist_ok=True)
                if output_dir.is_dir():
                    output_dir /= filename
                with output_dir.open("wb") as f:
                    f.write(response.content)

                logger.info(f"The asset (UUID: {uuid}) saved under the directory: {output_dir}")
                return str(output_dir)
            
        raise ValueError(f"Unable to fetch the asset of UUID: {uuid}.") 
    
    def show_asset(self, zip_path: str, model_name: str = "model.obj"):
        """Visualize an asset using trimesh.

        Args:
            zip_path (str): Path to zip file contained an asset
            model_name (str, optional): Name of an asset file. Defaults to "model.obj".
        """
        try:
            import trimesh
        except (ModuleNotFoundError, ImportError) as e:
            e.msg = (
                "Trimesh package not found. "
                "In order to visualize an asset install [vis] optional dependencies, "
                "e.g., pip install yellow-client[vis]."
            )
            raise e
        
        src_dir = Path(zip_path)
        dst_dir = src_dir.parent / src_dir.stem
        shutil.unpack_archive(src_dir, dst_dir)
        logger.info(f"Zip file {src_dir} extracted to {dst_dir}")
        
        obj_paths = []
        
        if (obj_path := dst_dir / model_name).exists():
            obj_paths.append(obj_path)
            
        if len(zip_paths := list(dst_dir.glob("*.zip"))) > 0:
            for zip_path in zip_paths:
                zip_dst_dir= zip_path.parent / zip_path.stem
                shutil.unpack_archive(zip_path, zip_dst_dir)
                logger.info(f"Zip file {zip_path} extracted to {zip_dst_dir}")
                obj_paths.append(zip_dst_dir / model_name)
        
        if len(uuid_obj_paths := list(dst_dir.glob("*.obj"))) > 0:
            for obj_path in uuid_obj_paths:
                obj_paths.append(obj_path)
                
        for obj_path in obj_paths:
            geometry = trimesh.load(obj_path)
            geometry.show()
 