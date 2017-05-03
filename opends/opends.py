#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import urllib
import gzip
import StringIO
import requests

opends_api_url_prefix = 'https://open.bdp.cn/api'
VERSION = "0.1.0"


class OpenDSException(Exception):
    pass


class OpenDS:
    token = None

    def __init__(self, token=None):
        self.url_prefix = opends_api_url_prefix
        requests.packages.urllib3.disable_warnings()
        self.token = token

    def _request(self, url, payload=None, param=None):
        if not payload:
            payload = {}
        if not param:
            param = {}
        param['_t'] = time.time()
        param['access_token'] = self.token

        headers = {
            'Content-type': 'text/html;charset=utf-8',
            'Content-Encoding': 'gzip',
            "User-Agent": "bdp-sdk-python, {version}".format(version=VERSION)
        }

        try_count = 0
        result = {}
        while True:
            try:
                params = u'%s' % urllib.urlencode(param)
                _url = "%s?%s" % (url, params)
                if payload:
                    payload_str = u'%s' % json.dumps(payload)
                    # gzip
                    s = StringIO.StringIO()
                    g = gzip.GzipFile(fileobj=s, mode='w')
                    g.write(payload_str)
                    g.close()

                    res = requests.post(_url, data=s.getvalue(), headers=headers, verify=False).text
                else:
                    res = requests.post(_url, headers=headers, verify=False).text
                result = json.loads(res)

                break
            except IOError, e:
                try_count += 1
                print u'can not connect to server, retry ... | reason: %s' % str(e)
                time.sleep(5)
                if try_count == 5:
                    raise e
            except Exception, e:
                raise e

        # print u'api:%s\t request_id:%s' % ('/'.join(url.split('/')[-2:]), result.get('request_id', ''))
        if not result:
            error_msg = "\nstatus: {status}\nerror_str: {errstr}\nrequest_id: {req_id}".format(
                status="-1",
                errstr="connection failed",
                req_id=""
            )
            raise OpenDSException(error_msg)

        if result['status'] != '0':

            error_msg = "\nstatus: {status}\nerror_str: {errstr}\nrequest_id: {req_id}".format(
                status=result['status'],
                errstr=result['errstr'],
                req_id=result.get('request_id', '')
            )
            raise OpenDSException(error_msg)
        return result['result']

    def ds_create(self, token, name):
        url = '%s/ds/create' % self.url_prefix
        params = {
            'access_token': token,
            'name': name,
            'type': 'opends'
        }
        return self._request(url, param=params)

    def ds_list(self, token):
        url = '%s/ds/list' % self.url_prefix
        params = {
            'access_token': token
        }
        return self._request(url, param=params)

    def ds_delete(self, token, ds_id):
        url = '%s/ds/delete' % self.url_prefix
        params = {
            'access_token': token,
            'ds_id': ds_id
        }
        return self._request(url, param=params)

    def tb_create(self, token, ds_id, name, schema, uniq_key, title=None):
        url = '%s/tb/create' % self.url_prefix
        params = {
            'access_token': token,
        }
        data = {
            'ds_id': ds_id,
            'name': name,
            'schema': schema,
            'uniq_key': uniq_key
        }
        if title:
            data['title'] = title

        return self._request(url, param=params, payload=data)

    def tb_name_modify(self, token, tb_id, alias_name):
        url = '%s/tb/modify' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'name': alias_name
        }
        return self._request(url, param=params)

    def tb_delete(self, token, tb_id):
        url = '%s/tb/delete' % self.url_prefix

        params = {
            'access_token': token,
            'tb_id': tb_id
        }
        return self._request(url, param=params)

    def tb_list(self, token, ds_id):
        url = '%s/tb/list' % self.url_prefix
        params = {
            'access_token': token,
            'ds_id': ds_id
        }
        return self._request(url, param=params)

    def tb_info(self, token, tb_id):
        url = '%s/tb/info' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id
        }
        return self._request(url, param=params)

    def tb_clean(self, token, tb_id):
        url = '%s/tb/clean' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id
        }
        return self._request(url, param=params)

    def tb_commit(self, token, tb_id):
        url = '%s/tb/commit' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fast': 0
        }
        return self._request(url, param=params)

    def tb_merge(self, token, tb_id):
        url = '%s/tb/commit' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fast': 0
        }
        return self._request(url, param=params)

    def tb_update(self, token, tb_ids):
        url = '%s/tb/update' % self.url_prefix
        params = {
            'access_token': token,
            'tb_ids': json.dumps(tb_ids)
        }
        return self._request(url, param=params)

    def tb_insert(self, token, tb_id, fields, data):
        url = '%s/tb/insert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields': json.dumps(fields)
        }
        return self._request(url, param=params, payload=data)

    def tb_insert_by_id(self, token, tb_id, fields, data):
        url = '%s/tb/insert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields_id': json.dumps(fields)
        }
        return self._request(url, param=params, payload=data)

    def data_insert(self, token, tb_id, fields, data):
        url = '%s/data/insert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields': json.dumps(fields)
        }
        return self._request(url, param=params, payload=data)

    def data_insert_by_id(self, token, tb_id, fields, data):
        url = '%s/data/insert' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields_id': json.dumps(fields)
        }
        return self._request(url, param=params, payload=data)

    def tb_preview(self, token, tb_id):
        url = '%s/tb/preview' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
        }
        return self._request(url, param=params)

    def field_list(self, token, tb_id):
        url = '%s/field/list' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id
        }
        return self._request(url, param=params)

    def field_del(self, token, tb_id, name):
        url = '%s/field/delete' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'name': name
        }
        return self._request(url, param=params)

    def field_add(self, token, tb_id, name, type, uniq_index, title=None):
        url = '%s/field/add' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'name': name,
            'type': type,
            'uniq_index': uniq_index
        }
        if title is not None:
            params["title"] = title

        return self._request(url, param=params)

    def field_modify(self, token, tb_id, name, f_type, uniq_index, title=None):
        url = '%s/field/modify' % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'name': name,
            'type': f_type,
            'uniq_index': uniq_index
        }
        if title is not None:
            params["title"] = title
        return self._request(url, param=params)

    def data_update(self, token, tb_id, fields, data):
        url = "%s/data/update" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields': json.dumps(fields)
        }

        return self._request(url, param=params, payload=data)

    def data_update_by_id(self, token, tb_id, fields, data):
        url = "%s/data/update" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields_id': json.dumps(fields)
        }

        return self._request(url, param=params, payload=data)

    def data_delete(self, token, tb_id, fields, data):
        url = "%s/data/delete" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields': json.dumps(fields)
        }

        return self._request(url, param=params, payload=data)

    def data_delete_by_id(self, token, tb_id, fields, data):
        url = "%s/data/delete" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'fields_id': json.dumps(fields)
        }

        return self._request(url, param=params, payload=data)

    def data_bulkdelete(self, token, tb_id, where):
        url = "%s/data/bulkdelete" % self.url_prefix
        params = {
            'access_token': token,
            'tb_id': tb_id,
            'where': where
        }
        return self._request(url, param=params)
