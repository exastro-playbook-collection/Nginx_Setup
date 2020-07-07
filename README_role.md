# Ansible Role: Nginx\_Setup

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

本Ansble Roleは"Nginx"の設定を行います。
対象バージョンは以下のバージョンです。

- RHEL 7

このRoleの実行前提はNginxが既にインストールされていることです。  
Ansibleのモジュールを利用して、以下の設定を行います。  

- nginx構成ファイル

## Supports

- 管理マシン(Ansibleサーバ)
  - Linux系OS（RHEL 7 または 8）
  - Ansible バージョン2.8 または 2.9
  - Python バージョン2.7 または 3.6
  - [crossplane V0.5.3](https://github.com/nginxinc/crossplane)

- 管理対象マシン(インストール対象マシン)
  - RHEL 7
  - Python バージョン2.7 または 3.6

## Requirements
  * 管理対象マシンとroot権限でSSH通信可能であること。

## Role Variables
### Mandatory Variables

以下の変数は必ず指定します。

- Nginx設定の関連変数
  * ''VAR\_Nginx\_server'': nginx構成ファイルのserverブロックを設定します (list)
      * ''isDelete'': 指定したserverブロックを削除するかどうか (boolean、例：true)
      * ''server\_name'': serverブロック名 (string, 例：mail.* www.server13.org、複数個があれば、半角スペースで区切ります)
      * ''location'': locationブロックを設定します (list)
          * ''isDelete'': 指定したlocationブロックを削除するかどうか，locationが定義されている場合は必須 (boolean、例：true)
          * ''name'': locationブロック名、locationが定義されている場合は必須 (string、例：  ~ /\.ht1)

### Optional variables

以下の変数は任意で指定します。
  * ''VAR\_Nginx\_tmpDir'': 一時ファイルが保存されるディレクトリ、半角スペースを含まないでください
  * ''VAR\_Nginx\_server'':
      * ''listen'': IPおよびポートでリッスンする (string、例：127.0.0.1:9098，IPとポートをコロンで区切ります)
      * ''root'': ルートディレクトリ (string、例：/www/data)
      * ''location'':
        * ''option'': locationブロックデータ (list、下記の例を参考のこと）：
          - root /data
          - proxy_pass http://www.example.com
          - sub_filter      /blog/ /blog-staging/
          - sub_filter
        * ''return'': locationブロックのreturn属性 (string、例：301 http://www.example.com/moved/here、複数個ある場合、半角スペースで区切ります)
      * ''serverFilePath'': serverブロックを格納するファイルへのパス (string、例：/home/site1/server1.conf)

## Dependencies

特にありません。

## Usage

1. 本Roleを用いたPlaybookを作成します。
2. 必須変数を指定します。  
3. 任意変数を必要に応じて指定します。
4. Playbookを実行します。

## Example Playbook

インストールとすべての設定をする場合は、提供した以下のRoleを"roles"ディレクトリに配置したうえで、
以下のようなPlaybookを作成してください。

- フォルダ構成
~~~
  - roles/
    ・ Nginx_Install/
    ・ Nginx_OSSetup/
    ・ Nginx_Setup/
  - hosts
  - Nginx.yml
  - conf.yml
~~~

- マスターPlaybook サンプル「Nginxsetup.yml」（Webサイトを作成・配置する場合）
~~~
# Nginx.yml
- hosts: Nginx
  roles:
    - role: Nginx_Setup
      VAR_Nginx_server
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
                - proxy_pass http://www.example.com
                - sub_filter      /blog/ /blog-staging/
                - sub_filter     'href="http://127.0.0.1:8080/'    'href="https://$host/'
                - sub_filter     'img src="http://127.0.0.1:8080/' 'img src="https://$host/'
                - error_page 404 =301 http:/example.com/new/path.html
              return: 301 http://www.example.com/moved/here
          serverFilePath: /usr/local/nginx/conf/site1Conf/server1.conf
        - isDelete: false
          server_name: example1.com www.example1.com
          listen: 127.0.0.1:8080
          root: /www/data1
          location:
            - isDelete: true
              name: /images11/
            - isDelete: false
              name: /images22/
              option:
                - root /data
                - proxy_pass http://www.example.com
                - sub_filter      /blog/ /blog-staging/
                - sub_filter     'href="http://127.0.0.1:8080/'    'href="https://$host/'
                - sub_filter     'img src="http://127.0.0.1:8080/' 'img src="https://$host/'
                - error_page 404 =301 http:/example.com/new/path.html
              return: 301 http://www.example.com/moved/here
          serverFilePath: /usr/local/nginx/conf/site1Conf/server2.conf
      tags:
        - Nginx_Setup
~~~

## Running Playbook
- extra-vars を利用する場合の実行例
~~~sh
ansible-playbook Nginx.yml -i hosts --extra-vars="@conf.yml"
~~~

- group_vars を利用する場合の実行例  
 group_vars で指定したグループ名が webserver1 の場合
~~~sh
ansible-playbook Nginx.yml -i hosts -l webserver1
~~~

- host_vars を利用する場合の実行例  
 host_vars で指定したグループ名が server1 の場合
~~~sh
ansible-playbook Nginx.yml -i hosts -l server1
~~~

- 本Roleのみを実行する場合は、 --tags "Nginx_Setup" を付け加える
~~~sh
ansible-playbook Nginx.yml -i hosts --extra-vars="@conf.yml" --tags "Nginx_Setup"
~~~

# Copyright
Copyright (c) 2020 NEC Corporation

# Author Information
NEC Corporation
