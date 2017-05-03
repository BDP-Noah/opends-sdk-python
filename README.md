# SDK for Python


A Python library for OpenAPI's HTTP-based Core APIs.

------

### 下载地址

[opends-sdk-python](https://update.bdp.cn/opends-sdk-python.zip)

### SDK安装

在本项目路径下执行 `$ python setup.py install`

### 注意事项
1. python支持版本：2.6/2.7
2. 字符编码使用UTF-8
3. 支持的数据类型：number, string, date(建议使用 %Y-%m-%d %H:%M:%S 格式)
4. 数据源名, 工作表名, 同一张表的不同字段名, title不可重复
5. 当前的架构设计对于频繁的小量数据写入处理效率不高，所以建议还是尽量批量的更新数据， 但是大量的数据传输会提高等待时间，因此建议尽量将数据量控制在5万条左右
6. ACCESS_TOKEN从BDP网站的开发者中心获取

### SDK简介
|   所属类  |         方法        |             说明             |
|:---------:|:-------------------:|:----------------------------:|
| BDPClient |      get_all_ds     |      获取所有数据源      |
|           |        get_ds       |          获取数据源          |
|           |      delete_ds      |          删除数据源          |
|           |      create_ds      |          创建数据源          |
|     DS    |    get_all_tables   | 获取该数据源的所有工作表 |
|           |     create_table    |          创建工作表          |
|           |     delete_table    |          删除工作表          |
|           |      get_table      |          获取工作表          |
|           |        update       |        更新相应工作表        |
|           |      update_all     |        更新所有工作表        |
|           |        get_id       |         获取数据源id         |
|           |       get_name      |        获取数据源名称        |
|   Table   | insert_data_by_name |           插入数据           |
|           |  insert_data_by_id  |           插入数据           |
|           |     bulk_delete     |         批量删除数据         |
|           | delete_data_by_name |          删除数据行          |
|           |  delete_data_by_id  |          删除数据行          |
|           | update_data_by_name |          更新数据行          |
|           |  update_data_by_id  |          更新数据行          |
|           |        commit       |        提交原始工作表        |
|           |        clean        |         清空该工作表         |
|           |      get_fields     |         列出所有字段         |
|           |      add_field      |         添加指定字段         |
|           |     delete_field    |         删除指定字段         |
|           |     modify_table    |         修改表的别名         |
|           |       preview       |           预览数据           |
|           |       get_info      |          获取表信息          |
|           |        get_id       |           获取表id           |
|           |       get_name      |          获取表名称          |
|           |     modify_field    |         修改字段属性         |
### SDK说明

- #### BDPClient
    用于初始化客户端，进行数据源增、删、查操作等等。

  构造方法

    - `BDPClient(ACCESS_TOKEN)`

    - 使用:

    ```python
    from opends.sdk import BDPClient
    client = BDPClient(ACCESS_TOKEN)
    ```

  实例方法

    - `get_all_ds()` 获取所有数据源对象，返回键为名字，值为相应数据源对象的字典。

        - 返回值: `{"ds_name": ds}`

        -  使用:

        ```python
        all_ds = client.get_all_ds()
        ```

    - `get_ds(name)` 根据名字获取数据源，返回数据源对象
        - 参数:
          <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
            </tr>
            <tr>
              <td>name</td>
              <td>string</td>
            </tr>
          </table>

        - 返回值: `ds(DS object)`

        -  使用:

        ```python
        ds = client.get_ds("ds_name")
        ```

    - `delete_ds(name)` 根据名字删除数据源

        - 参数:
          <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
            </tr>
            <tr>
              <td>name</td>
              <td>string</td>
            </tr>
          </table>

        -  使用:

        ```python
        client.delete_ds("ds_name")
        ```

    - `create_ds(name)` 根据名字创建数据源，返回创建的数据源对象

        - 参数:
          <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
            </tr>
            <tr>
              <td>name</td>
              <td>string</td>
            </tr>
          </table>

        - 返回值: `ds(DS object)`

        -  使用:

        ```python
        ds = client.create_ds("ds_name")
        ```

- #### DS

    数据源类，可以管理该数据源内的各种工作表，并对工作表进行增、删、改、查等操作。
    >通过调用BDPClient类的create_ds方法来创建DS对象,不能通过直接实例化DS类来创建数据源.
    >通过调用BDPClient类的get_ds方法来获取相应的DS对象.

  构造方法

    - `DS(name, token)`

  实例方法

    - `get_all_tables()` 获取该数据源的所有工作表对象，返回键为表名，值为工作表对象的字典

        - 返回值: `{"table_name": table}`

        -  使用:

        ```python
        all_tables = ds.get_all_tables()
        ```

    - `create_table(name, schema, uniq_key=None)` 在该数据源中创建工作表，返回该工作表, schema中的type只能是"string"/"number"/"date"其中一种。对于每个字段的设定，remark和title参数可以缺省。

        - 参数:

          <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>name</td>
              <td>string</td>
              <td>否</td>
            </tr>
            <tr>
              <td>schema</td>
              <td>list</td>
              <td>否</td>
            </tr>
            <tr>
              <td>uniq_key</td>
              <td>list</td>
              <td>是</td>
            </tr>
            <tr>
              <td>title</td>
              <td>string</td>
              <td>是</td>
            </tr>
          </table>

        -  使用:

        ```python
        schema = [
            {
                "remark": "",
                "name": "id",
                "type": "number",
                "title": "ident"
            },
            {
                "remark": "",
                "name": "name",
                "type": "string"
            },
            {
                "remark": "",
                "name": "height",
                "type": "number"
            },
            {
                "remark": "",
                "name": "join_time",
                "type": "date"
            },
            {
                "remark": "",
                "name": "mark",
                "type": "string",
                "title": "words"
            }
        ]
        table = ds.create("table_name", schema=schema, uniq_key=["id"], title="my_table")
        ```

    - `delete_table(name)` 根据名字删除工作表

        - 参数:

            <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
            </tr>
            <tr>
              <td>name</td>
              <td>string</td>
            </tr>
          </table>

        - 使用:

        ```python
        ds.delete_table("table_name")
        ```

    - `get_table(name)` 根据名字获取工作表

        - 参数:

            <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
            </tr>
            <tr>
              <td>name</td>
              <td>string</td>
            </tr>
          </table>

        - 使用:

        ```python
        table = ds.get_table("table_name")
        ```

    - `update(tb_ids)` 根据工作表id列表更新相应工作表

        - 参数:

            <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
            </tr>
            <tr>
              <td>tb_ids</td>
              <td>list</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb_ids = ["tb_id1", "tb_id2"]
        ds.update(tb_ids)
        ```

    - `update_all()` 级联更新该数据源的下的所有工作表
        - 使用:

        ```python
        ds.update_all()
        ```

    - `get_id()` 获取数据源id

        - 返回值: `ds_dh83hd2hd23jd32bi`

        - 使用:

        ```python
        ds_id = ds.get_id()
        ```

    - `get_name()` 获取数据源名称

        - 返回值: `ds_name`

        - 使用:

        ```python
        ds_name = ds.get_name()
        ```

- #### Table

    工作表类，对工作表进行增、删、改的操作。
    > 通过调用DS类的create_table方法而不是通过实例化Table类来创建新表。
    > 通过调用DS类的get_table方法来获取相应表的Table实例。

  构造方法

    - `Table(ds, name, tb_id, schema=(), uniq_key=None)`

  实例方法

    - `insert_data_by_name(fields, data)` 向指定的字段插入数据，根据字段名

        - 参数:

        <table>
          <tr>
            <th>参数</th>
            <th>类型</th>
            <th>可缺省</th>
          </tr>
          <tr>
            <td>fields</td>
            <td>list</td>
            <td>否</td>
          </tr>
          <tr>
            <td>data</td>
            <td>list</td>
            <td>否</td>
          </tr>
        </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        fields = ["id", "name", "age"]
        data = [[1, "user1", 13], [2, "user2", 14]]
        tb.insert_data_by_name(fields, data)
        ```

    - `insert_data_by_id(fields, data)` 向指定的字段插入数据，根据字段id

        - 参数:

          <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>fields</td>
              <td>list</td>
              <td>否</td>
            </tr>
            <tr>
              <td>data</td>
              <td>list</td>
              <td>否</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        fields = ["fksada22", "fksae322", "fks832dh23"]
        data = [[1, "user1", 13], [2, "user2", 14]]
        tb.insert_data_by_id(fields, data)
        ```

    - `bulk_delete(where)` 根据where条件批量删除数据

        - 参数:

          <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>where</td>
              <td>string</td>
              <td>否</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        where = "`id` > 3"
        where2 = "`name` = 'Tom'"
        tb.bulk_delete(where)
        tb.bulk_delete(where2)
        ```

    - `delete_data_by_name(fields, data)` 根据fields列表中的字段名删除数据行

        - 参数:

           <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>fields</td>
              <td>list</td>
              <td>否</td>
            </tr>
            <tr>
              <td>data</td>
              <td>list</td>
              <td>否</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        fields = ["id", "name", "age"]
        data = [[1, "user1", 13], [2, "user2", 14]]
        tb.delete_data_by_name(fields, data)
        ```

    - `delete_data_by_id(fields, data)` 根据fields列表中的字段id删除数据行

        - 参数:

           <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>fields</td>
              <td>list</td>
              <td>否</td>
            </tr>
            <tr>
              <td>data</td>
              <td>list</td>
              <td>否</td>
            </tr>
          </table>
        - 使用:

        ```python
        tb = ds.get_table("table_name")
        fields = ["fksada22", "fksae322", "fks832dh23"]
        data = [[1, "user1", 13], [2, "user2", 14]]
        tb.delete_data_by_id(fields, data)
        ```

    - `update_data_by_name(fields, data)`  根据fields列表中的字段名更新数据行

        - 参数:

           <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>fields</td>
              <td>list</td>
              <td>否</td>
            </tr>
            <tr>
              <td>data</td>
              <td>list</td>
              <td>否</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        fields = ["id", "name", "age"]
        data = [[1, "user1", 13], [2, "user2", 14]]
        tb.update_data_by_name(fields, data)
        ```

    - `update_data_by_id(fields, data)`  根据fields列表中的字段id更新数据行

        - 参数:

           <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>fields</td>
              <td>list</td>
              <td>否</td>
            </tr>
            <tr>
              <td>data</td>
              <td>list</td>
              <td>否</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        fields = ["fksada22", "fksae322", "fks832dh23"]
        data = [[1, "user1", 13], [2, "user2", 14]]
        tb.update_data_by_id(fields, data)
        ```

    - `commit()` 提交原始工作表

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        tb.commit()
        ```

    - `clean()` 清空该工作表

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        tb.clean()
        ```

    - `get_fields()` 列出所有字段

        - 返回值:

        ```python
        [
            {
                "name": "xxx",
                "uniq_index": 0/1,
                "type": "number"/"string"/"date",
                "field_id": "fksada32",
                "remark": ""
            },
            {...}
        ]
        ```

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        fields = tb.get_fields()
        ```

    - `add_field(field_name, field_type, uniq_index=0, title=None)` 添加指定字段, field_type只能是"string"/"number"/"date"其中一种。uniq_index为1表示该字段为主键，0为非主键, title为字段别名。

        - 参数:

           <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>field_name</td>
              <td>string</td>
              <td>否</td>
            </tr>
            <tr>
              <td>field_type</td>
              <td>string</td>
              <td>否</td>
            </tr>
            <tr>
              <td>uniq_index</td>
              <td>int</td>
              <td>是</td>
            </tr>
            <tr>
              <td>title</td>
              <td>string</td>
              <td>是</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        tb.add_field("field_name", "string", 0, "alias_field")
        ```

    - `delete_field(field_name)` 删除指定字段

        - 参数:

           <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>field_name</td>
              <td>string</td>
              <td>否</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        tb.delete_field("field_name")
        ```

    - `modify_table(alias_name)` 修改表的别名（在web端显示的名称)
        - `alias_name: alias_name (字符串)`

        - 参数:

           <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>alias_name</td>
              <td>string</td>
              <td>否</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        tb.modify_table("alias_name")
        ```

    - `modify_field(field_name, field_type, uniq_index=0, title=None)` 修改字段属性,field_type只能是"string"/"number"/"date"其中一种。uniq_index为1表示该字段为主键，0为非主键， title为字段别名。

        - 参数:

           <table>
            <tr>
              <th>参数</th>
              <th>类型</th>
              <th>可缺省</th>
            </tr>
            <tr>
              <td>field_name</td>
              <td>string</td>
              <td>否</td>
            </tr>
            <tr>
              <td>field_type</td>
              <td>string</td>
              <td>否</td>
            </tr>
            <tr>
              <td>uniq_index</td>
              <td>int</td>
              <td>是</td>
            </tr>
            <tr>
              <td>title</td>
              <td>string</td>
              <td>是</td>
            </tr>
          </table>

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        tb.modify_field("field_name", "string", 0, "alias_field")
        ```

    - `preview()` 预览数据

        - 返回值:

        ```python
        {
            "schema" [
                {
                    "name": "id",
                    "type": "string",
                    "uniq_index": 0,
                    "remark": ""
                },
                {...}
            ],
            "data": [...],
            "data_count": 3,
            "utime": "2015-03-24 18:02:36"
            "status": 0,
            "materialized": 1,
            "can_partition": False,
            "partition": None
        }
        ```

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        result = tb.preview()
        ```

    - `get_info()` 获取表信息

        - 返回值:

        ```python
        {
            "fields": [
                {
                    "name": "xxx",
                    "field_id": "fdsa8783",
                    "title": "",
                    "type": "string"
                },
                {...}
            ],
            "tb_id": "tb_id",
            "name": "name",
            "data_count": 100,
            "title": "date_test"
        }
        ```

        - 使用:

        ```python
        tb = ds.get_table("table_name")
        result = tb.get_info()
        ```

    - `get_id()` 获取表id

        - 返回值: `tb_dh83hd2hd23jd32bi`

        - 使用:

        ```python
        tb_id = tb.get_id()
        ```

    - `get_name()` 获取表名称

        - 返回值: `tb_name`

        - 使用:

        ```python
        tb_name = tb.get_name()
        ```

### 异常信息
1. 所有的服务器端异常都将抛出包含错误码以及错误信息的OpenDSException，错误码可以参照API文档

2. 本地的异常将直接抛出带错误信息的OpenDSException

### 示例

- 获取指定数据源对象并获取其中所有的工作表

  ```python
  from opends.sdk import BDPClient

  c = BDPClient(ACCESS_TOKEN)

  ds = c.get_ds("ds_example")

  all_tables = ds.get_all_tables()
  ```
