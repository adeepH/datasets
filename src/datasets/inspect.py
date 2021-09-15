# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
""" List and inspect datasets and metrics."""

from typing import Dict, List, Optional, Union

from .hf_api import HfApi
from .load import import_main_class, prepare_module
from .utils import DownloadConfig
from .utils.download_manager import GenerateMode
from .utils.logging import get_logger
from .utils.version import Version


logger = get_logger(__name__)


def list_datasets(with_community_datasets=True, with_details=False):
    """List all the datasets scripts available on HuggingFace AWS bucket.

    Args:
        with_community_datasets (``bool``, optional, default ``True``): Include the community provided datasets.
        with_details (``bool``, optional, default ``False``): Return the full details on the datasets instead of only the short name.
    """
    api = HfApi()
    return api.dataset_list(with_community_datasets=with_community_datasets, id_only=bool(not with_details))


def list_metrics(with_community_metrics=True, with_details=False):
    """List all the metrics script available on HuggingFace AWS bucket

    Args:
        with_community_metrics (Optional ``bool``): Include the community provided metrics (default: ``True``)
        with_details (Optional ``bool``): Return the full details on the metrics instead of only the short name (default: ``False``)
    """
    api = HfApi()
    return api.metric_list(with_community_metrics=with_community_metrics, id_only=bool(not with_details))


def inspect_dataset(path: str, local_path: str, download_config: Optional[DownloadConfig] = None, **download_kwargs):
    r"""
    Allow inspection/modification of a dataset script by copying on local drive at local_path.

    Args:
        path (``str``): path to the dataset processing script with the dataset builder. Can be either:

            - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``
            - a dataset identifier on HuggingFace AWS bucket (list all available datasets and ids with ``datasets.list_datasets()``)
                e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``
        local_path (``str``): path to the local folder to copy the datset script to.
        download_config (Optional ``datasets.DownloadConfig``: specific download configuration parameters.
        **download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied.
    """
    module_path, _ = prepare_module(
        path, download_config=download_config, dataset=True, force_local_path=local_path, **download_kwargs
    )
    print(
        f"The processing script for dataset {path} can be inspected at {local_path}. "
        f"The main class is in {module_path}. "
        f"You can modify this processing script and use it with `datasets.load_dataset({local_path})`."
    )


def inspect_metric(path: str, local_path: str, download_config: Optional[DownloadConfig] = None, **download_kwargs):
    r"""
    Allow inspection/modification of a metric script by copying it on local drive at local_path.

    Args:
        path (``str``): path to the dataset processing script with the dataset builder. Can be either:

            - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``
            - a dataset identifier on HuggingFace AWS bucket (list all available datasets and ids with ``datasets.list_datasets()``)
                e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``
        local_path (``str``): path to the local folder to copy the datset script to.
        download_config (Optional ``datasets.DownloadConfig``: specific download configuration parameters.
        **download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied.
    """
    module_path, _ = prepare_module(
        path, download_config=download_config, dataset=False, force_local_path=local_path, **download_kwargs
    )
    print(
        f"The processing scripts for metric {path} can be inspected at {local_path}. "
        f"The main class is in {module_path}. "
        f"You can modify this processing scripts and use it with `datasets.load_metric({local_path})`."
    )


def get_dataset_infos(
    path: str,
    script_version: Optional[Union[str, Version]] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    force_local_path: Optional[str] = None,
    dynamic_modules_path: Optional[str] = None,
    return_resolved_file_path: bool = False,
    return_associated_base_path: bool = False,
    data_files: Optional[Union[Dict, List, str]] = None,
    **download_kwargs,
):
    """Get the meta information about a dataset, returned as a dict mapping config name to DatasetInfoDict.

    Args:
        path (``str``): path to the dataset processing script with the dataset builder. Can be either:

            - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``
            - a dataset identifier on HuggingFace AWS bucket (list all available datasets and ids with ``datasets.list_datasets()``)
                e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``
        script_version (Optional ``Union[str, datasets.Version]``):
            If specified, the dataset module will be loaded from the datasets repository at this version.
            By default:
            - it is set to the local version of the lib.
            - it will also try to load it from the master branch if it's not available at the local version of the lib.
            Specifying a version that is different from your local version of the lib might cause compatibility issues.
        download_config (:class:`DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        force_local_path (Optional str): Optional path to a local path to download and prepare the script to.
            Used to inspect or modify the script folder.
        dynamic_modules_path (Optional str, defaults to HF_MODULES_CACHE / "datasets_modules", i.e. ~/.cache/huggingface/modules/datasets_modules):
            Optional path to the directory in which the dynamic modules are saved. It must have been initialized with :obj:`init_dynamic_modules`.
            By default the datasets and metrics are stored inside the `datasets_modules` module.
        return_resolved_file_path (Optional bool, defaults to False):
            If True, the url or path to the resolved dataset is returned with the other outputs
        return_associated_base_path (Optional bool, defaults to False):
            If True, the base path associated to the dataset is returned with the other outputs.
            It corresponds to the directory or base url where the dataset script/dataset repo is at.
        data_files (:obj:`Union[Dict, List, str]`, optional): Defining the data_files of the dataset configuration.
        download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied,
            for example ``use_auth_token``
    """
    module_path, _ = prepare_module(
        path,
        dataset=True,
        script_version=script_version,
        download_config=download_config,
        download_mode=download_mode,
        force_local_path=force_local_path,
        dynamic_modules_path=dynamic_modules_path,
        return_resolved_file_path=return_resolved_file_path,
        return_associated_base_path=return_associated_base_path,
        data_files=data_files,
        **download_kwargs,
    )
    builder_cls = import_main_class(module_path, dataset=True)
    return builder_cls.get_all_exported_dataset_infos()


def get_dataset_config_names(
    path: str,
    script_version: Optional[Union[str, Version]] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    force_local_path: Optional[str] = None,
    dynamic_modules_path: Optional[str] = None,
    return_resolved_file_path: bool = False,
    return_associated_base_path: bool = False,
    data_files: Optional[Union[Dict, List, str]] = None,
    **download_kwargs,
):
    """Get the list of available config names for a particular dataset.

    Args:
        path (``str``): path to the dataset processing script with the dataset builder. Can be either:

            - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
                e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``
            - a dataset identifier on HuggingFace AWS bucket (list all available datasets and ids with ``datasets.list_datasets()``)
                e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``
        script_version (Optional ``Union[str, datasets.Version]``):
            If specified, the dataset module will be loaded from the datasets repository at this version.
            By default:
            - it is set to the local version of the lib.
            - it will also try to load it from the master branch if it's not available at the local version of the lib.
            Specifying a version that is different from your local version of the lib might cause compatibility issues.
        download_config (:class:`DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, default ``REUSE_DATASET_IF_EXISTS``): Download/generate mode.
        force_local_path (Optional str): Optional path to a local path to download and prepare the script to.
            Used to inspect or modify the script folder.
        dynamic_modules_path (Optional str, defaults to HF_MODULES_CACHE / "datasets_modules", i.e. ~/.cache/huggingface/modules/datasets_modules):
            Optional path to the directory in which the dynamic modules are saved. It must have been initialized with :obj:`init_dynamic_modules`.
            By default the datasets and metrics are stored inside the `datasets_modules` module.
        return_resolved_file_path (Optional bool, defaults to False):
            If True, the url or path to the resolved dataset is returned with the other outputs
        return_associated_base_path (Optional bool, defaults to False):
            If True, the base path associated to the dataset is returned with the other outputs.
            It corresponds to the directory or base url where the dataset script/dataset repo is at.
        data_files (:obj:`Union[Dict, List, str]`, optional): Defining the data_files of the dataset configuration.
        download_kwargs: optional attributes for DownloadConfig() which will override the attributes in download_config if supplied,
            for example ``use_auth_token``
    """
    module_path, _ = prepare_module(
        path,
        dataset=True,
        script_version=script_version,
        download_config=download_config,
        download_mode=download_mode,
        force_local_path=force_local_path,
        dynamic_modules_path=dynamic_modules_path,
        return_resolved_file_path=return_resolved_file_path,
        return_associated_base_path=return_associated_base_path,
        data_files=data_files,
        **download_kwargs,
    )
    builder_cls = import_main_class(module_path, dataset=True)
    return list(builder_cls.builder_configs.keys())
