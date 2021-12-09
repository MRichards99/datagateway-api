from abc import ABC, abstractclassmethod
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    validator,
)


class PaNOSCAttribute(ABC, BaseModel):
    @abstractclassmethod
    def from_icat(self):
        pass


class Affiliation(PaNOSCAttribute):
    """Information about which facility a member is located at"""

    id_: StrictStr = Field(alias="id")
    name: Optional[StrictStr]
    address: Optional[StrictStr]
    city: Optional[StrictStr]
    country: Optional[StrictStr]

    members: Optional[List["Member"]]

    @classmethod
    def from_icat(cls):
        pass


class Dataset(PaNOSCAttribute):
    """
    Information about an experimental run, including optional File, Sample, Instrument
    and Technique
    """

    pid: StrictStr
    title: StrictStr
    is_public: StrictBool = Field(alias="isPublic")
    creation_date: datetime = Field(alias="creationDate")
    score: Decimal

    documents: List["Document"]
    techniques: List["Technique"]
    instrument: Optional["instrument"]
    files: Optional[List["File"]]
    parameters: Optional[List["Parameter"]]
    samples: Optional[List["Sample"]]

    @classmethod
    def from_icat(cls):
        pass


class Document(PaNOSCAttribute):
    """
    Proposal which includes the dataset or published paper which references the dataset
    """

    pid: StrictStr
    is_public: StrictBool = Field(alias="isPublic")
    type_: StrictStr = Field(alias="type")
    title: StrictStr
    summary: Optional[StrictStr]
    doi: Optional[StrictStr]
    start_date: Optional[datetime] = Field(alias="startDate")
    end_date: Optional[datetime] = Field(alias="endDate")
    release_date: Optional[datetime] = Field(alias="releaseDate")
    license_: Optional[StrictStr] = Field(alias="license")
    keywords: Optional[List[StrictStr]]
    score: Decimal

    datasets: List[Dataset]
    members: Optional[List["Member"]]
    parameters: Optional[List["Parameter"]]

    @classmethod
    def from_icat(cls):
        pass


class File(PaNOSCAttribute):
    """Name of file and optionally location"""

    id_: StrictStr = Field(alias="id")
    name: StrictStr
    path: Optional[StrictStr]
    size: Optional[StrictInt]

    dataset: Dataset

    @classmethod
    def from_icat(cls):
        pass


class Instrument(PaNOSCAttribute):
    """Beam line where experiment took place"""

    id_: StrictStr = Field(alias="id")
    name: StrictStr
    facility: StrictStr
    score: Decimal

    datasets: Optional[List[Dataset]]

    @classmethod
    def from_icat(cls):
        pass


class Member(PaNOSCAttribute):
    """Proposal team member or paper co-author"""

    id_: StrictStr = Field(alias="id")
    role: Optional[StrictStr] = Field(alias="role")

    # Should a member be able to be part of many documents?
    document: Document
    person: Optional["Person"]
    affiliations: Optional[List[Affiliation]]

    @classmethod
    def from_icat(cls):
        pass


class Parameter(PaNOSCAttribute):
    """
    Scalar measurement with value and units.
    Note: a parameter is either related to a dataset or a document, but not both.
    """

    id_: StrictStr = Field(alias="id")
    name: StrictStr
    value: Union[StrictFloat, StrictInt, StrictStr]
    unit: Optional[StrictStr]

    dataset: Optional[Dataset]
    document: Optional[Document]

    @validator(
        "document", always=True,
    )
    def validate_dataset_and_document(cls, value, values):  # noqa: B902, N805
        # TODO - Should there be a check for if both document and dataset are None?

        if "dataset" in values and values["dataset"] is not None and value is not None:
            # TODO - Should an exception be raised here instead?
            return None

        return value

    @classmethod
    def from_icat(cls):
        pass


class Person(PaNOSCAttribute):
    """Human who carried out experiment"""

    id_: StrictStr = Field(alias="id")
    full_name: StrictStr = Field(alias="fullName")
    orcid: Optional[StrictStr]
    researcher_id: Optional[StrictStr] = Field(alias="researcherId")
    first_name: Optional[StrictStr] = Field(alias="firstName")
    last_name: Optional[StrictStr] = Field(alias="lastName")

    # ICAT has InvestigationUser meaning a user can have multiple roles, one for each
    # investigation
    member: Optional[Member]

    @classmethod
    def from_icat(cls):
        pass


class Sample(PaNOSCAttribute):
    """Extract of material used in the experiment"""

    name: StrictStr
    # ID used as an identifier in example implementation
    pid: Optional[StrictStr]
    description: Optional[StrictStr]

    datasets: Optional[List[Dataset]]

    @classmethod
    def from_icat(cls):
        pass


class Technique(PaNOSCAttribute):
    """Common name of scientific method used"""

    pid: StrictStr
    name: StrictStr

    datasets: Optional[List[Dataset]]

    @classmethod
    def from_icat(cls):
        pass


# The below models reference other models that may not be defined during their
# creation so their references have to manually be updated to lead to the actual
# models or else an exception will be raised. This can be done with the help of
# the postponed annotations via the future import together with the
# `update_forward_refs` method, only after all related models are declared.
Affiliation.update_forward_refs()
Dataset.update_forward_refs()
Document.update_forward_refs()
Member.update_forward_refs()