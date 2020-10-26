"""
This view include the business logic for huu config tool, defines all functionality related to workspace
"""
from django.views.generic.base import TemplateView
from django.db import IntegrityError
import models
import sys
from django.shortcuts import render, redirect
from components import models as c_models
from django.db import DatabaseError
import datetime, os, time, json, subprocess, shutil
from components import models as c_models
import svn.remote
from website import settings
from components.models import Platform
from django.http import HttpResponse
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from django.http import FileResponse
import tarfile

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def progress(filename, size, sent):
    print filename + " " + str(size) + " " + str(sent)


class AuthenticationPsk():
    password = {}

    def __init__(self, password_auth, user_auth):
        AuthenticationPsk.password[str(user_auth)] = password_auth


class Workspace(TemplateView):
    template_name = 'workspace/workspace.html'

    def get_user_workspace(self):
        print __name__ + ".py :", sys._getframe().f_code.co_name
        try:
            ws_list = models.user_workspace.objects.filter(added_by=self.request.session['users'])
        except:
            ws_list = ''
            DatabaseError
        return ws_list

    def get_release_list(self):
        try:
            release_list = models.release_list.objects.all()
        except:
            release_list = ''
            DatabaseError
        return release_list

    def get_context_data(self, **kwargs):
        context = super(Workspace, self).get_context_data(**kwargs)
        context['ws_list'] = self.get_user_workspace()
        context['release_list'] = self.get_release_list()
        return context


class ManageRelease(TemplateView):
    template_name = 'workspace/add_release.html'

    def get_user_workspace(self):
        try:
            ws_list = "list"
        except IntegrityError as e:
            print "#" * 5, "Error : ", e.message
        return ws_list

    def get(self, request, *args, **kwargs):
        response_data = {}
        try:
            release_list = models.release_list.objects.all()
        except:
            release_list = ''
            DatabaseError
        response_data['release_list'] = release_list
        return render(request, self.template_name, response_data)

    def post(self, request, *args, **kwargs):
        response_data = {}
        rel_name = request.POST.get("rel_name")
        svn_path = request.POST.get("svn_path")
        uname = request.POST.get("uname")
        print("release_list= " + release_list + "release= " + release, "svn_url=", svn_url, "added_by=", added_by)
        try:
            release_list = models.release_list.objects.create(release=rel_name, svn_url=svn_path.strip(),
                                                              added_by=uname)
        except:
            release_list = ''
            DatabaseError
        try:
            release_list = models.release_list.objects.all()
        except:
            release_list = ''
            DatabaseError
        response_data['release_list'] = release_list

        return render(request, self.template_name, response_data)

    def get_context_data(self, **kwargs):
        context = super(ManageRelease, self).get_context_data(**kwargs)
        context['ws_list'] = self.get_user_workspace()
        return context


# def get_context_data(self, **kwargs):
#     if 'view' not in kwargs:
#         kwargs['view'] = self
#     return kwargs

def add_common_tool(request):
    response_data = {}

    if request.method == 'POST':
        document = request.FILES['document']
        toolName = request.POST['toolName']  # +



        filepath = os.path.join(request.session['ws_path'], 'third_party/tools_rhel', 'COMMON', toolName.strip('/'))
        u_path = os.path.join(request.session['ws_path'], 'third_party/tools_rhel')
        if not os.path.exists(u_path):
            os.makedirs(u_path)
        location = filepath, u_path
        print ">>>>>>>>>>", filepath


        #newtool = models.tool_list.objects.create(toolName=toolName, location=u_path, softLocation='/root')
        #newtool.save()



        with open(filepath, 'wb+') as dest:
            for chunk in document.chunks():
                dest.write(chunk)

        return HttpResponseRedirect('workspace/add_common_tool/')

    #tool_list = models.tool_list.objects.all()
    #response_data["tool_list"] =  tool_list

    return render(request, 'workspace/add_common_tool.html', response_data)


def add_pid(request):
    response_data = {}

    if request.method == 'POST':
        document = request.FILES['document']
        specfileName = request.POST['specfileName']  # + extension

        filepath = os.path.join(settings.ws_path.strip('/'),specfileName.strip('/'))
        u_path = os.path.join(settings.ws_path.strip('/'))
        if not os.path.exists(u_path):
            os.makedirs(u_path)
        location = filepath, u_path
        print ">>>>>>>>>>", filepath


        #newtool = Tool.objects.create(toolName=specfile, location=upload_path, softLocation=destination)
        #newtool.save()



        with open(filepath, 'wb+') as dest:
            for chunk in document.chunks():
                dest.write(chunk)

        return HttpResponseRedirect('/components/toollist/')
    # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

    return render(request, 'workspace/add_pciid.html', response_data)


def add_workspace(request):
    response_data = {}
    uname = request.session['users']
    ws_name = request.POST.get('ws_name')
    release = request.POST.get('release')
    add_date = datetime.datetime.now().date()

    print __name__ + ".py :", sys._getframe().f_code.co_name
    try:
        release_list = models.release_list.objects.get(release=release)
    except:
        release_list = ''
        DatabaseError
    try:
        models.user_workspace.objects.get(ws_name=ws_name)
    #         response_data['msg'] = "Project name already exists."
    #         response_data['status'] = False
    #         return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        DatabaseError
    #     time.sleep(10)

    # os.system("cp "+settings.ws_path+"/"+"Remote_db"+"/"+"db.sqlite3"+" "+path+"/")
    # print ("svn --non-interactive --trust-server-cert --username "+uname+" --password "+" co "+str(release_list.svn_url.strip()))

    # print ("Password = ",AuthenticationPsk.password[str(uname)])
    try:
        r = svn.remote.RemoteClient(str(release_list.svn_url.strip()), username=uname,
                                password=AuthenticationPsk.password[str(uname)])
    except Exception as e:
        print("Password was not there in global variable " + str(e))
        response_data['msg'] = "For creating new workspace please logout and login again."
        response_data['status'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


    path = settings.ws_path + "/" + uname + "_" + ws_name
    print("** this we have to add a local path and svn should checkout in that path=", path)
    if os.path.exists(path):
        response_data['msg'] = "Project name already exists."
        response_data['status'] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        os.makedirs(path)
    print("here i can add code path=", path, "url=", str(release_list.svn_url.strip()))

    msg = r.checkout(path)
    try:
        models.user_workspace.objects.create(ws_name=ws_name, release=release_list, \
                                             svn_url=str(release_list.svn_url), added_by=uname, add_date=add_date,
                                             ws_path=path)
    except:
        release_list = ''
        DatabaseError

    settings.DATABASE_APPS_MAPPING = {'components': uname + "_" + ws_name, }
    database_id = uname + "_" + ws_name  # just something unique
    newDatabase = {}
    newDatabase["id"] = database_id
    newDatabase['ENGINE'] = 'django.db.backends.sqlite3'
    newDatabase['NAME'] = path + '/deltas/post-build/rootfs/root/CBL/DB/db.sqlite3'
    # newDatabase['NAME'] = path+'/db.sqlite3'
    newDatabase['USER'] = ''
    newDatabase['PASSWORD'] = ''
    newDatabase['HOST'] = ''
    newDatabase['PORT'] = ''
    settings.DATABASES[database_id] = newDatabase

    #     save_db_settings_to_file(newDatabase)
    response_data['msg'] = "Project created successfully    ."
    response_data['status'] = True
    request.session['ws_name'] = ws_name
    request.session['release'] = release
    response_data['ws_name'] = ws_name
    request.session['ws_path'] = path
    response_data['release'] = release
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def move_ws(request):
    response_data = {}
    ws_name = request.POST.get('ws_name')
    release = request.POST.get('release')
    id_ip = request.POST.get('id_ip').encode('UTF-8')
    id_path = request.POST.get('id_path').encode('UTF-8')
    id_username = request.POST.get('id_username').encode('UTF-8')
    id_password = request.POST.get('id_password').encode('UTF-8')

    print __name__ + ".py :", sys._getframe().f_code.co_name

    try:
        res = models.user_workspace.objects.get(ws_name=ws_name, added_by=request.session['users'])
        ws_path = res.ws_path

    except:
        DatabaseError
        os.system("rm -rf " + ws_path + ".tar.gz")
        response_data['msg'] = "Database error..."
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    print("ws_name :", (request.session['users'] + "_" + ws_name).encode("UTF-8"), "ws_path :", ws_path.encode("UTF-8"))
    make_tarfile(
        settings.ws_path.encode("UTF-8") + "/" + (request.session['users'] + "_" + ws_name).encode("UTF-8") + ".tar.gz",
        ws_path.encode("UTF-8"))

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())


    try:
        ssh.connect(id_ip, port=22, username=id_username, password=id_password)
        # SCPCLient takes a paramiko transport as its only argument
        # Just a no-op. Required sanitize function to allow wildcards.
        scp = SCPClient(ssh.get_transport(), sanitize=lambda x: x, progress=progress)

        try:
            scp.put(""+ws_path+".tar.gz", remote_path=str(id_path) , recursive=False)
        except Exception as x:
            print(x)
            os.system("rm -rf " + ws_path + ".tar.gz")
            response_data['msg'] = "Workspace not moved as..." + str(
                x) + " ip = " + id_ip + " path = " + id_path + " user = " + id_username
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as x:
        print(x)
        os.system("rm -rf " + ws_path + ".tar.gz")
        response_data['msg'] = "Workspace not moved as..." + str(
            x) + " ip = " + id_ip + " path = " + id_path + " user = " + id_username
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    try:
        res.delete()
    except:
        DatabaseError
    try:
        shutil.rmtree(ws_path, ignore_errors=True)
    except:
        DatabaseError

    cmd = "rm -rf "+ws_path+".tar.gz"
    res1 = subprocess.check_output(cmd, shell=True)
    print "\n\n>>>>>>>>", res1
    if res1 == 0:
        response_data['msg'] = "Workspace moved successfully..."
        response_data['status'] = True
    else:
        response_data['msg'] = "Failed building ISO... \nCheck log for details."
        response_data['status'] = False


    #os.system()
    response_data['msg'] = "Workspace moved successfully..."
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_ws(request):
    response_data = {}
    ws_name = request.POST.get('ws_name')
    release = request.POST.get('release')
    print __name__ + ".py :", sys._getframe().f_code.co_name
    try:
        res = models.user_workspace.objects.get(ws_name=ws_name, added_by=request.session['users'])
        ws_path = res.ws_path
        res.delete()
    except:
        DatabaseError
    try:
        shutil.rmtree(ws_path, ignore_errors=True)
    except:
        DatabaseError
    response_data['msg'] = "Workspace deleted successfully..."
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def redirect_to_components(request, ws_name, release):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    try:
        res = models.user_workspace.objects.get(ws_name=ws_name, added_by=request.session['users'])
    except:
        DatabaseError
        print("", ws_name, request.session['users'],
              models.user_workspace.objects.get(ws_name=ws_name, added_by=request.session['users']))
        print DatabaseError

    request.session['ws_name'] = ws_name
    request.session['release'] = release
    request.session['ws_path'] = res.ws_path
    return redirect('index', ws_name, release)


def create_iso(request):
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name
    response_data = {}
    response_data['allPlatforms'] = allPlatforms

    if request.method == 'POST' and request.is_ajax():
        platform = request.POST.get('platform')
        container = request.POST.get('container')
        container_version = request.POST.get('container_version')
        vic_container = request.POST.get('vic_container')
        vic_fw_version = request.POST.get('vic_fw_version')
        bios_version = request.POST.get('bios_version')
        try:
            res = models.user_workspace.objects.get(ws_name=request.session['ws_name'])
        except:
            DatabaseError

        cmd = "cd " + res.ws_path + " && sh build_rhel_huu.sh -p " + str(platform) + " -u " + str(
            container) + " -v " + str(container_version) + " -l '" + str(vic_container) + "' -V '" + str(
            vic_fw_version) + "' -B '" + str(bios_version) + "' 2>&1 | tee build.log && cd -"

        print("Cmd going to trigger =",cmd)

        res1 = subprocess.check_output(cmd, shell=True)
        print "\n\n>>>>>>>>", res1
        if res1 == 0:
            response_data['msg'] = "Building ISO completed..."
            response_data['status'] = True
        else:
            response_data['msg'] = "Failed building ISO... \nCheck log for details."
            response_data['status'] = False
            print("sending  --- ")
            print(json.dumps(response_data))
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    #      ./build_rhel_huu.sh -p PL1  -c /root/Desktop/C220M5-3.1.1cS5.zip -v 3.1.1cS5 -l "http://cspg-download.cisco.com/ucs-b-series/cruz-dev-builds/svn_latest/Images.5/fw/" -V "4.1(3.157)" -B "3.1.1.5"

    from django.utils.encoding import smart_str
    res = models.user_workspace.objects.get(ws_name=request.session['ws_name'], added_by=request.session['users'])
    try:
        res = models.user_workspace.objects.get(ws_name=request.session['ws_name'])
    except:
        DatabaseError
    iso_path = os.path.join(res.ws_path, 'buildroot-2013.05/output/images/rootfs.iso')
    if not os.path.exists(iso_path):
        response_data['msg'] = "ISO not created."
        response_data['iso_exists'] = 'false'
    else:
        response_data['iso_exists'] = 'true'
        response_data['msg'] = "ISO created."
    return render(request, 'workspace/create_iso.html', response_data)


def get_log(request):
    response_data = {}
    try:
        res = models.user_workspace.objects.get(ws_name=request.session['ws_name'])
    except:
        DatabaseError
    f_name = res.ws_path + "/build.log"
    print f_name
    with open(f_name) as log:
        res = log.readlines()
    response_data['log'] = res
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_iso_status(request):
    response_data = {}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def download_iso(request):
    response_data = {}
    from django.utils.encoding import smart_str
    try:
        res = models.user_workspace.objects.get(ws_name=request.session['ws_name'])
    except:
        res = models.user_workspace.objects.get(ws_name='new16')
        DatabaseError

    iso_path = os.path.join(res.ws_path, 'buildroot-2013.05/output/images/rootfs.iso')

    #     if not os.path.exists(iso_path):
    #         response_data['msg'] = "Project name already exists."
    #         response_data['status'] = False
    #         return HttpResponse(json.dumps(response_data), content_type="application/json")
    fsock = open(iso_path, "rb")
    #response = HttpResponse(fsock, content_type='application/zip')
    response = FileResponse(fsock, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=huuiso.iso'
    response['X-Sendfile'] = smart_str(iso_path) # jatin
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response

def downloadjson(request):
    ws_path = request.session['ws_path']
    print("******--  HERE -----*****")

    print __name__ + ".py :", sys._getframe().f_code.co_name

    if 'platform' in request.GET:
        message = 'You searched for: %r' % request.GET['platform']
    else:
        message = 'You submitted an empty form.'
    print(message)
    platform = request.GET['platform']

    content_disposition = 'attachment; filename=' + str(platform) + ".json"

    os.system("rm " + ws_path + "/deltas/post-build/rootfs/root/CBL/JSON/" + str(platform) + "_catalog.json")
    print(
            "python2.7 " + ws_path + "/deltas/post-build/rootfs/root/CBL/Utilities/CBL_Db2Json.py " + ws_path + "/deltas/post-build/rootfs/root/CBL/DB/db.sqlite3 " + str(
        platform).upper() + " > " + ws_path + "/deltas/post-build/rootfs/root/CBL/JSON/" + str(
        platform) + "_catalog.json")
    os.system(
        "python2.7 " + ws_path + "/deltas/post-build/rootfs/root/CBL/Utilities/CBL_Db2Json.py " + ws_path + "/deltas/post-build/rootfs/root/CBL/DB/db.sqlite3 " + str(
            platform).upper() + " > " + ws_path + "/deltas/post-build/rootfs/root/CBL/JSON/" + str(
            platform) + "_catalog.json")

    json_data = open(ws_path + '/deltas/post-build/rootfs/root/CBL/JSON/' + str(platform) + '_catalog.json', "r").read()
    # response_data = {"data": json.loads(json_data), "file_name": "%s.json" % str(platform)}
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = content_disposition
    return response
