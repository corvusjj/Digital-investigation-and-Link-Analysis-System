from entities.location import Location, Address
from entities.communication import Message, Call, SocialMediaPost, IPSession
from entities.digital_evidence import File, Image, Video
from entities.digital_identity import Email, PhoneNumber, Username, SocialMediaAccount, OnlineAccount, CloudAccount
from entities.financial import BankAccount, Transaction, Bank
from entities.forensic import Weapon, Substance, Fingerprint, DNASample, Document
from entities.network import Device, IPAddress, MACAddress, WifiNetwork, Server, Domain, Website
from entities.people import Person, Organization, Group
from entities.physical import Vehicle, LicensePLate, Property, PhysicalObject
from entities.other import Event, Case

ENTITY_REGISTRY = {
    "LOCATION": {
        "LOCATION": Location,
        "ADDRESS": Address
    },
    "COMMUNICATION": {
        "MESSAGE": Message,
        "CALL": Call,
        "SOCIAL MEDIA POST": SocialMediaPost,
        "IP SESSION": IPSession
    },
    "DIGITAL EVIDENCE": {
        "FILE": File,
        "IMAGE": Image,
        "VIDEO": Video
    },
    "DIGITAL IDENTITY": {
        "EMAIL": Email,
        "PHONE NUMBER": PhoneNumber,
        "USERNAME": Username,
        "SOCIAL MEDIA ACCOUNT": SocialMediaAccount,
        "ONLINE ACCOUNT": OnlineAccount,
        "CLOUD ACCOUNT": CloudAccount
    },
    "FINANCIAL": {
        "BANK ACCOUNT": BankAccount,
        "TRANSACTION": Transaction,
        "BANK": Bank
    },
    "FORENSIC": {
        "WEAPON": Weapon,
        "SUBSTANCE": Substance,
        "FINGERPRINT": Fingerprint,
        "DNA SAMPLE": DNASample,
        "DOCUMENT": Document
    },
    "NETWORK": {
        "DEVICE": Device,
        "IP ADDRESS": IPAddress,
        "MAC ADDRESS": MACAddress,
        "WIFI NETWORK": WifiNetwork,
        "SERVER": Server,
        "DOMAIN": Domain,
        "WEBSITE": Website
    },
    "PEOPLE": {
        "PERSON": Person,
        "ORGANIZATION": Organization,
        "GROUP": Group
    },
    "PHYSICAL": {
        "VEHICLE": Vehicle,
        "LICENSE PLATE": LicensePLate,
        "PROPERTY": Property,
        "PHYSICAL OBJECT": PhysicalObject
    },
    "OTHER": {
        "EVENT": Event,
        "CASE": Case
    }
}
 