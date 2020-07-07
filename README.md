# Nginx

# Trademarks
-----------
* Linuxは、Linus Torvalds氏の米国およびその他の国における登録商標または商標です。
* RedHat、RHEL、CentOSは、Red Hat, Inc.の米国およびその他の国における登録商標または商標です。
* Windows、PowerShellは、Microsoft Corporation の米国およびその他の国における登録商標または商標です。
* Ansibleは、Red Hat, Inc.の米国およびその他の国における登録商標または商標です。
* pythonは、Python Software Foundationの登録商標または商標です。
* Nginxは、Nginx Software Inc. の米国登録商標です。
* Crossplaneは、Upbound, Inc.の登録商標または商標です。
* NECは、日本電気株式会社の登録商標または商標です。
* その他、本ロールのコード、ファイルに記載されている会社名および製品名は、各社の登録商標または商標です。

## Description
本プロジェクトのリポジトリでNginxのインストール、設定、OS設定Roleを公開しています。  
詳細は、各ディレクトリのREADME_role.mdを参照ください。  
対象バージョンは以下のバージョンとなります。  
・nginx-1.16.1  
  
対応OSは以下となります。  
・RHEL 7  
  
## Roleを利用して、一括でNginxのインストールと設定とOS設定を実施する
RoleごとにNginxのインストールと設定およびOS設定を行うことができますが、一括でNginxをインストールと設定、OS設定を行うこともできます。
以下は一括でNginxをインストール・設定し、OS設定を行うPlaybookの構成や利用方法を説明します。

１．構成の例：

~~~~
Playbook                      # 対象ソース（playbook）
 |-- roles
 |    |-- Nginx_Install       # Nginxインストールの用Role
 |    |-- Nginx_OSSetup       # Nginx OS設定用Role
 |    `-- Nginx_Setup         # Nginx設定用Role
 |-- Nginx.yml                # Playbookのメインファイル
 |-- hosts                    # ホストファイル
 `-- README.md
~~~~

２．Playbookの例：

~~~
#Nginx.yml
---
- hosts: Nginx
  roles:
    - role: Nginx_Install
      VAR_Nginx_yumInstall: true
    - role: Nginx_OSSetup
      VAR_Nginx_status: start
      VAR_Nginx_auto: true
    - role: Nginx_Setup
      VAR_Nginx_server: 
        - isDelete: true
          server_name: server1.com
        - isDelete: false
          server_name: server2.com
          listen: 127.0.0.1:80
          root: /www/data
          location:
            - isDelete: true
              name: /
            - isDelete: false
              name: /images11/
              option:
                - root /data
              return: 301 http://www.example.com/moved/here
          serverFilePath: /usr/local/nginx/conf/site1Conf/server1.conf
~~~

# Copyright
Copyright (c) 2020 NEC Corporation

# Author Information
NEC Corporation
