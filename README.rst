==============
Fs2web
==============

1. Introduction_
2. Requirements_
3. Installation_

Introduction
============

**Fs2web** is the Django_ based Web UI for FreeSWITCH_.

.. _Django: http://www.djangoproject.com/
.. _FreeSWITCH: http://freeswitch.org

Requirements
============

- Django >= 1.0
- FreeSWITCH - svn trunk

Installation
============

Запуск - cd fs2web; ./manage.py runserver

Для редактирования настроек надо зайти в административный интерфейс: http://127.0.0.1:8000/admin/
Логин admin, пароль kuku.

В conf/autoload_configs/xml_curl.conf.xml:


<configuration name="xml_curl.conf" description="cURL XML Gateway">
  <bindings>
    <binding name="fs2web_user_fetcher">
        <param name="gateway-url" value="http://127.0.0.1:8000/user/get/" bindings="directory"/>
    </binding>
    <binding name="fs2web_dialplan_fetcher">
        <param name="gateway-url" value="http://127.0.0.1:8000/dialplan/get/" bindings="dialplan"/>
    </binding>
  </bindings>
</configuration>



И включить загрузку модуля xml_curl в conf/autoload_configs/modules.conf.xml 

