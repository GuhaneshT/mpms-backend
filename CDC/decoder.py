import struct
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Column:
    name: str
    type_id: int
    value: Optional[str]

@dataclass
class Relation:
    relation_id: int
    schema: str
    table: str
    columns: list[Column]

@dataclass
class ChangeEvent:
    op: str
    schema: str
    table: str
    lsn: str
    data: dict
    old_data: dict

class PgOutputDecoder:
    def __init__(self):
        self.relations: dict[int, Relation] = {}

    def decode(self, payload: bytes, lsn: str) -> Optional[ChangeEvent]:
        
        if not payload:
            return None
        msg_type = chr(payload[0])
        if msg_type == 'B':
            return None
        elif msg_type == 'C':
            return None
        elif msg_type == 'R':
            self._decode_relation(payload)
            return None
        elif msg_type == 'I':
            return self._decode_insert(payload, lsn)
        elif msg_type == 'U':
            return self._decode_update(payload, lsn)
        elif msg_type == 'D':
            return self._decode_delete(payload, lsn)
        else:
            return None

    def _decode_relation(self, payload: bytes):
        offset = 1
        relation_id = struct.unpack_from('!I', payload, offset)[0]
        offset += 4
        schema, offset = self._read_string(payload, offset)
        table, offset = self._read_string(payload, offset)
        offset += 1
        num_columns = struct.unpack_from('!H', payload, offset)[0]
        offset += 2
        columns = []
        for _ in range(num_columns):
            offset += 1
            col_name, offset = self._read_string(payload, offset)
            type_id = struct.unpack_from('!I', payload, offset)[0]
            offset += 4
            offset += 4
            columns.append(Column(name=col_name, type_id=type_id, value=None))
        self.relations[relation_id] = Relation(
            relation_id=relation_id,
            schema=schema,
            table=table,
            columns=columns
        )

    def _decode_insert(self, payload: bytes, lsn: str) -> ChangeEvent:
        offset = 1
        relation_id = struct.unpack_from('!I', payload, offset)[0]
        offset += 4
        offset += 1
        relation = self.relations[relation_id]
        data, _ = self._decode_tuple(payload, offset, relation)
        return ChangeEvent(
            op='insert',
            schema=relation.schema,
            table=relation.table,
            lsn=lsn,
            data=data,
            old_data={}
        )

    def _decode_update(self, payload: bytes, lsn: str) -> ChangeEvent:
        offset = 1
        relation_id = struct.unpack_from('!I', payload, offset)[0]
        offset += 4
        relation = self.relations[relation_id]
        old_data = {}
        indicator = chr(payload[offset])
        offset += 1
        if indicator in ('O', 'K'):
            old_data, offset = self._decode_tuple(payload, offset, relation)
            offset += 1
        data, _ = self._decode_tuple(payload, offset, relation)
        return ChangeEvent(
            op='update',
            schema=relation.schema,
            table=relation.table,
            lsn=lsn,
            data=data,
            old_data=old_data
        )

    def _decode_delete(self, payload: bytes, lsn: str) -> ChangeEvent:
        offset = 1
        relation_id = struct.unpack_from('!I', payload, offset)[0]
        offset += 4
        relation = self.relations[relation_id]
        offset += 1
        data, _ = self._decode_tuple(payload, offset, relation)
        return ChangeEvent(
            op='delete',
            schema=relation.schema,
            table=relation.table,
            lsn=lsn,
            data=data,
            old_data={}
        )

    def _decode_tuple(self, payload: bytes, offset: int, relation: Relation):
        num_columns = struct.unpack_from('!H', payload, offset)[0]
        offset += 2
        row = {}
        for i in range(num_columns):
            col_type = chr(payload[offset])
            offset += 1
            if col_type == 'n':
                row[relation.columns[i].name] = None
            elif col_type == 'u':
                row[relation.columns[i].name] = None
            elif col_type == 't':
                length = struct.unpack_from('!I', payload, offset)[0]
                offset += 4
                value = payload[offset:offset + length].decode('utf-8')
                offset += length
                row[relation.columns[i].name] = value
        return row, offset

    def _read_string(self, payload: bytes, offset: int) -> tuple[str, int]:
        end = payload.index(b'\x00', offset)
        value = payload[offset:end].decode('utf-8')
        return value, end + 1