from ..flow.types_group_flow import TypesGroupsFlow


class TypesGroupsCore:

    @classmethod
    def __init__(cls) -> None:
        pass

    @classmethod
    def create_types_group(cls, data):
        return TypesGroupsFlow.types_groups_handeler("create", data)

    @classmethod
    def edite_types_group(cls, data):
        return TypesGroupsFlow.types_groups_handeler("update",data, data["group_code"])

    @classmethod
    def get_types_group(cls, data):
        return TypesGroupsFlow.types_groups_handeler("select", data)

    @classmethod
    def get_all_types_group(cls, data):
        return TypesGroupsFlow.types_groups_handeler("select_all", data)

    @classmethod
    def delete_types_group(cls, data):
        return TypesGroupsFlow.types_groups_handeler("delete", data["key"], data["value"])
