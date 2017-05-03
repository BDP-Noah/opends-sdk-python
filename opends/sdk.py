#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .opends import OpenDS, OpenDSException
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Table(object):
    def __init__(self, ds, name, tb_id, schema=(), uniq_key=None, title=None):
        """
            the table object for bdp
        Args:
            ds (DS):
            name (str):
        """
        if not name:
            raise OpenDSException(u'Table name is required.')
        if not ds and not type(ds) != DS:
            raise OpenDSException(u'Ds is required.')
        self._name = name

        # remove duplicate field(dict) if exist in schema(list)
        self._schema = [dict(n) for n in set([tuple(s.items()) for s in schema])]
        self._uniq_key = uniq_key
        self._ds = ds
        self._tb_id = tb_id
        if tb_id:
            if schema == ():
                pass
            else:
                self.modify_schema()
        else:
            self._tb_id = self._ds.opends.tb_create(None, self._ds.ds_id, name, self._schema, uniq_key, title).get('tb_id')

    def modify_schema(self):
        """
            modify the table schema, add field or delete failed.
        """
        schema_used = self._ds.opends.field_list(None, self._tb_id)
        schema_used_name = map(lambda field: field.get('name'), schema_used)
        schema_conf_name = map(lambda field: field.get('name'), self._schema)

        _need_add = filter(lambda field: field.get('name') not in schema_used_name, self._schema)
        _need_del = filter(lambda field: field.get('name') not in schema_conf_name, schema_used)

        for fd in _need_del:
            try:
                self._ds.opends.field_del(None, self._tb_id, fd.get('name'))
            except Exception, e:
                print u'Delete field `%s` failed and ignored, reason: %s' % (fd.get('name'), e)

        for fd in _need_add:
            try:
                self._ds.opends.field_add(None, self._tb_id, fd.get('name'), fd.get('type'), 0)
            except Exception, e:
                print u'Add field `%s` failed and ignored, reason: %s' % (fd.get('name'), e)

    @property
    def name(self):
        return self._name

    @property
    def uniq_key(self):
        return self._uniq_key

    @property
    def ds(self):
        return self._ds

    @property
    def tb_id(self):
        return self._tb_id

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    def get_name(self):
        return self._name

    def get_id(self):
        return self._tb_id

    def insert_data_by_name(self, fields, data):
        """
            add data to current table
        :param fields: (list) eg: ["id", "name", "age"]
        :param data: (list) eg: [[1, "user", 30],[2, "user2", 31]]
        :return:
        """
        self._ds.opends.data_insert(None, self._tb_id, fields, data)
        return True

    def insert_data_by_id(self, fields, data):
        """
            add data to current table
        :param fields: (list) eg: ["id", "name", "age"]
        :param data: (list) eg: [[1, "user", 30],[2, "user2", 31]]
        :return:
        """
        self._ds.opends.data_insert_by_id(None, self._tb_id, fields, data)
        return True

    def insert_table_by_name(self, fields, data):
        """
            add data to current table
        :param fields: (list) eg: ["id", "name", "age"]
        :param data: (list) eg: [[1, "user", 30],[2, "user2", 31]]
        :return:
        """
        self._ds.opends.tb_insert(None, self._tb_id, fields, data)
        return True

    def insert_table_by_id(self, fields, data):
        """
            add data to current table
        :param fields: (list) eg: ["id", "name", "age"]
        :param data: (list) eg: [[1, "user", 30],[2, "user2", 31]]
        :return:
        """
        self._ds.opends.tb_insert_by_id(None, self._tb_id, fields, data)
        return True

    def bulk_delete(self, where):
        """
            bulk delete data from current table according to `where`
        :param where: (string) eg: "`id` > 3"
        :return:
        """
        self._ds.opends.data_bulkdelete(None, self._tb_id, where)
        return True

    def delete_data_by_name(self, fields, data):
        """
            delete data according to field name
        :param fields: (list)
        :param data: (list)
        :return:
        """
        self._ds.opends.data_delete(None, self._tb_id, fields, data)
        return True

    def delete_data_by_id(self, fields, data):
        """
            delete data according to field id
        :param fields: (list)
        :param data: (list)
        :return:
        """
        self._ds.opends.data_delete_by_id(None, self._tb_id, fields, data)
        return True

    def update_data_by_name(self, fields, data):
        """
            update data according to field name
        :param fields: (list)
        :param data: (list)
        :return:
        """
        self._ds.opends.data_update(None, self._tb_id, fields, data)
        return True

    def update_data_by_id(self, fields, data):
        """
            update data according to field id
        :param fields: (list)
        :param data: (list)
        :return:
        """
        self._ds.opends.data_update_by_id(None, self._tb_id, fields, data)
        return True

    def commit(self):
        self._ds.opends.tb_commit(None, self._tb_id)
        return True

    def clean(self):
        self._ds.opends.tb_clean(None, self._tb_id)

    def get_fields(self):
        return self._ds.opends.field_list(None, self._tb_id)

    def add_field(self, field_name, field_type, uniq_index=0, title=None):
        """
            add one field to current table
        :param field_name: (string)
        :param field_type:  (string) "string"/"number"/"date"
        :param uniq_index:  (number) 0/1
        :param title: (string)
        :return:
        """
        if not field_name:
            raise OpenDSException("field_name required")
        if field_type not in ["string", "number", "date"]:
            raise OpenDSException("wrong field_type")
        if uniq_index not in [0, 1]:
            raise OpenDSException("uniq_index can only be 0 or 1")
        self._ds.opends.field_add(None, self._tb_id, field_name, field_type, uniq_index, title)
        return True

    def modify_field(self, field_name, field_type, uniq_index=0, title=None):
        """
            modify one field of current table
        :param field_name: (string)
        :param field_type: (string) "string"/"number"/"date"
        :param uniq_index: (number) 0/1
        :param title: (string)
        :return:
        """
        if not field_name:
            raise OpenDSException("field_name required")
        if field_type not in ["string", "number", "date"]:
            raise OpenDSException("wrong field_type")
        if uniq_index not in [0, 1]:
            raise OpenDSException("uniq_index can only be 0 or 1")
        self._ds.opends.field_modify(None, self._tb_id, field_name, field_type, uniq_index, title)
        return True

    def delete_field(self, field_name):
        """
            delete one field of current table
        :param field_name: (string)
        :return:
        """
        if not field_name:
            raise OpenDSException("field name required")
        self._ds.opends.field_del(None, self._tb_id, field_name)
        return True

    def modify_table(self, alias_name):
        """
            modify the alias name of current table
        :param alias_name: (string)
        :return:
        """
        if not alias_name:
            raise OpenDSException("table alias name required")
        self._ds.opends.tb_name_modify(None, self._tb_id, alias_name)
        return True

    def preview(self):
        return self._ds.opends.tb_preview(None, self._tb_id)

    def get_info(self):
        return self._ds.opends.tb_info(None, self._tb_id)


class DS(object):
    def __init__(self, name, token=None):
        """
            the database object for bdp
        Args:
            name:
            token:
        """
        if not name:
            raise OpenDSException(u'DS name is required.')
        self._name = name
        self._opends = OpenDS(token)
        self._ds_id = None
        self.tables = {}
        for ds in self._opends.ds_list(None)['data_source']:
            if name == ds['name']:
                self._ds_id = ds['ds_id']
                for table in ds['tables']:
                    self.tables[table[0]] = Table(self, table[0], table[1])
                break

        if not self._ds_id:
            self._ds_id = self._opends.ds_create(None, name)["ds_id"]

    @property
    def opends(self):
        return self._opends

    @property
    def name(self):
        return self._name

    @property
    def ds_id(self):
        return self._ds_id

    @property
    def tb_ids(self):
        return [tb.tb_id for tb in self.tables.values()]

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    def get_name(self):
        return self._name

    def get_id(self):
        return self._ds_id

    def get_all_tables(self):
        return self.tables

    def create_table(self, name, schema, uniq_key=None, title=None):
        """
            create a table in current ds
        :param name: (string)
        :param schema: (list) eg: [{"comment": "", "name": "user", "type": "string"}, {"comment": "", "name": "id", "type": "number"}, {"comment": "", "name": "age", "type": "number"}]
        :param uniq_key: (list) eg: ["id"]
        :return:
        """
        if not isinstance(name, unicode):
            try:
                name = name.decode("utf-8")
            except Exception:
                raise OpenDSException("name can only be string")
        if not isinstance(schema, list):
            raise OpenDSException("schema can only be list")
        if len(schema):
            if isinstance(schema[0], list):
                schema = self._gen_schema(schema)
        table = Table(self, name, tb_id=None, schema=schema, uniq_key=uniq_key, title=title)
        self.tables.update({name: table})
        return table

    def _gen_schema(self, schema):
        res = []
        for s in schema:
            if len(s) == 2:
                res.append({"name": s[0], "type": s[1]})
            elif len(s) == 3:
                res.append({"name": s[0], "type": s[1], "comment": s[2]})
            elif len(s) == 4:
                res.append({"name": s[0], "type": s[1], "comment": s[2], "title": s[3]})

        return res

    def delete_table(self, name):
        """
            delete one table
        :param name: (string)
        :return:
        """
        if not isinstance(name, unicode):
            try:
                name = name.decode("utf-8")
            except Exception:
                raise OpenDSException("name can only be string")
        try:
            tb_id = self.get_table(name).tb_id
        except Exception:
            raise OpenDSException('table not exists： %s' % name)
        self._opends.tb_delete(None, tb_id)
        del self.tables[name]
        return True

    def get_table(self, name):
        if not isinstance(name, unicode):
            try:
                name = name.decode("utf-8")
            except Exception:
                raise OpenDSException("name can only be string")
        res = self.tables.get(name)
        if res is None:
            raise OpenDSException("table not exists: {name}".format(name=name))
        return res

    def destroy(self):
        self._opends.ds_delete(None, self._ds_id)
        return True

    def update_all(self):
        """
            Trigger cascading update
        """
        self._opends.tb_update(None, [tb.tb_id for tb in self.tables.values()])
        return True

    def update(self, tb_ids):
        self._opends.tb_update(None, tb_ids)
        return True


class BDPClient:
    def __init__(self, token=None):
        if token is None:
            raise OpenDSException("no access_token,initial failed")
        self.token = token
        self._opends = OpenDS(token)
        self._ds_dict = {}
        for ds in self._opends.ds_list(None)['data_source']:
            self._ds_dict.update({ds["name"]: DS(ds['name'], token)})

    def get_all_ds(self):
        return self._ds_dict

    def get_ds(self, name):
        if not isinstance(name, unicode):
            try:
                name = name.decode("utf-8")
            except Exception:
                raise OpenDSException("name can only be string")
        if self._ds_dict.get(name) is None:
            raise OpenDSException("ds not exists：%s" % name)
        return self._ds_dict.get(name)

    def create_ds(self, name=None):
        """
            create new data source
        :param name: (string)
        :return:
        """
        if name is None:
            raise OpenDSException("name can't be None")
        if not isinstance(name, unicode):
            try:
                name = name.decode("utf-8")
            except Exception:
                raise OpenDSException("name can only be string")
        if self._ds_dict.get(name) is not None:
            raise OpenDSException("%s ds already exists" % name)

        self._ds_dict.update({name: DS(name, self.token)})
        return self._ds_dict.get(name)

    def delete_ds(self, name=None):
        """
            delete one data source
        :param name: (string)
        :return:
        """
        if not isinstance(name, unicode):
            try:
                name = name.decode("utf-8")
            except Exception:
                raise OpenDSException("name can only be string")
        if not self.get_ds(name) is None:
            self.get_ds(name).destroy()
            del self._ds_dict[name]
        else:
            raise OpenDSException(u'ds not exists: `%s`' % name)


# 暂时不开放以下


class SimpleClient:
    def __init__(self, token=None):
        if token is None:
            raise OpenDSException('token is required')
        self.token = token
        self._opends = OpenDS(token)
        self._ds_dict = {}
        dss = self._opends.ds_list(None)['data_source']
        for ds in dss:
            self._ds_dict.update({ds['name']: ds['ds_id']})

    def create_ds(self, name=None):
        if name is None:
            raise OpenDSException('ds name is reqiured')
        else:
            return self._opends.ds_create(None, name)['ds_id']

    def delete_ds(self, name):

        if name is None:
            raise OpenDSException('ds name is required')

        ds_id = self._ds_dict.get(name)
        if ds_id is None:
            raise OpenDSException('no ds names %s' % name)
        try:
            self._opends.ds_delete(None, ds_id)
        except Exception, e:
            raise OpenDSException(e)

    def list_ds(self):
        return self._opends.ds_list(None)['data_source']

    def create_table(self, ds_name, table_name, schema, uniq_key):
        ds_id = self._ds_dict.get(ds_name)
        if ds_id:
            try:
                return self._opends.tb_create(None, ds_id, table_name, schema, uniq_key)['tb_id']
            except Exception, e:
                raise OpenDSException(e)
        else:
            raise OpenDSException('ds %s is not exists')

    def insert_data(self, table_id, fields, data):
        try:
            self._opends.tb_insert(None, table_id, fields, data)
        except Exception, e:
            raise OpenDSException(e)

    def preview(self, table_id):
        try:
            return self._opends.tb_preview(None, table_id)
        except Exception, e:
            raise OpenDSException(e)

    def list_table(self, ds_name):
        ds_id = self._ds_dict.get(ds_name)
        if ds_id:
            return self._opends.tb_list(None, ds_id)
        else:
            raise OpenDSException('ds %s is not exists' % ds_name)

    def clean_table(self, table_id):
        try:
            self._opends.tb_clean(None, table_id)
        except Exception, e:
            raise OpenDSException(e)

    def delete_table(self, table_id):
        try:
            self._opends.tb_delete(None, table_id)
        except Exception, e:
            raise OpenDSException(e)

    def update_ds(self, ds_name):
        tables = self.list_table(ds_name)
        tb_ids = [t["tb_id"] for t in tables]
        self._opends.tb_update(None, tb_ids)

    def commit(self, table_id):
        self._opends.tb_commit(None, table_id)

    def modify_table_name(self, table_id, alias_name):
        self._opends.tb_name_modify(None, table_id, alias_name)

    def get_table_info(self, table_id):
        return self._opends.tb_info(None, table_id)

    def add_field(self, table_id, field_name, field_type, uniq_index, title=None):
        try:
            self._opends.field_add(None, table_id, field_name, field_type, uniq_index, title)
        except Exception, e:
            raise OpenDSException(e)

    def delete_field(self, table_id, field_name):
        try:
            self._opends.field_del(None, table_id, field_name)
        except Exception, e:
            raise OpenDSException(e)

    def list_field(self, table_id):
        return self._opends.field_list(None, table_id)

    def modify_field(self, table_id, field_name, field_type, uniq_index, title=None):
        try:
            self._opends.field_modify(None, table_id, field_name, field_type, uniq_index, title)
        except Exception, e:
            raise OpenDSException(e)

    def bulk_delete(self, table_id, where):
        try:
            self._opends.data_bulkdelete(None, table_id, where)
        except Exception, e:
            raise OpenDSException(e)

    def update_data(self, table_id, fields, data):
        try:
            self._opends.data_update(None, table_id, fields, data)
        except Exception, e:
            raise OpenDSException(e)

    def delete_data(self, table_id, fields, data):
        try:
            self._opends.data_delete(None, table_id, fields, data)
        except Exception, e:
            raise OpenDSException(e)
