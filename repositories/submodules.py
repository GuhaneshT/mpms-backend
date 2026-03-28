from supabase import Client
from uuid import UUID


# Table name mapping for submodule models
SUBMODULE_TABLES = {
    "ProductionChart": "production_charts",
    "AncillaryEquipment": "ancillary_equipment",
    "SiteVerification": "site_verifications",
    "PackingList": "packing_lists",
    "MaterialVerification": "material_verifications",
    "InstallationRecord": "installation_records",
}


class SubmoduleRepository:
    def __init__(self, client: Client, table_name: str):
        self.client = client
        self.table_name = table_name

    def get_by_order(self, order_id: UUID) -> dict | None:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .eq("order_id", str(order_id))
            .maybe_single()
            .execute()
        )
        return response.data

    def create(self, create_schema) -> dict:
        data = create_schema.model_dump(mode="json")
        # Handle enum fields (e.g., status in SiteVerification)
        for key, value in data.items():
            if hasattr(value, "value"):
                data[key] = value.value
        response = self.client.table(self.table_name).insert(data).execute()
        return response.data[0]

    def update(self, order_id: UUID, update_data) -> dict:
        update_dict = update_data.model_dump(exclude_unset=True, mode="json")
        for key, value in update_dict.items():
            if hasattr(value, "value"):
                update_dict[key] = value.value
        response = (
            self.client.table(self.table_name)
            .update(update_dict)
            .eq("order_id", str(order_id))
            .execute()
        )
        return response.data[0]

    def delete(self, order_id: UUID):
        self.client.table(self.table_name).delete().eq("order_id", str(order_id)).execute()
