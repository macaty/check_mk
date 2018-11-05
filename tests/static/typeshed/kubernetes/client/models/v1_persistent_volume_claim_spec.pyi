# Stubs for kubernetes.client.models.v1_persistent_volume_claim_spec (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1PersistentVolumeClaimSpec:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    access_modes: Any = ...
    data_source: Any = ...
    resources: Any = ...
    selector: Any = ...
    storage_class_name: Any = ...
    volume_mode: Any = ...
    volume_name: Any = ...
    def __init__(self, access_modes: Optional[Any] = ..., data_source: Optional[Any] = ..., resources: Optional[Any] = ..., selector: Optional[Any] = ..., storage_class_name: Optional[Any] = ..., volume_mode: Optional[Any] = ..., volume_name: Optional[Any] = ...) -> None: ...
    @property
    def access_modes(self): ...
    @access_modes.setter
    def access_modes(self, access_modes: Any) -> None: ...
    @property
    def data_source(self): ...
    @data_source.setter
    def data_source(self, data_source: Any) -> None: ...
    @property
    def resources(self): ...
    @resources.setter
    def resources(self, resources: Any) -> None: ...
    @property
    def selector(self): ...
    @selector.setter
    def selector(self, selector: Any) -> None: ...
    @property
    def storage_class_name(self): ...
    @storage_class_name.setter
    def storage_class_name(self, storage_class_name: Any) -> None: ...
    @property
    def volume_mode(self): ...
    @volume_mode.setter
    def volume_mode(self, volume_mode: Any) -> None: ...
    @property
    def volume_name(self): ...
    @volume_name.setter
    def volume_name(self, volume_name: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...