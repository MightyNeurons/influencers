from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .form import Advertisement_Form, Ad_Search
from .models import Advertisement_Create
from django.shortcuts import redirect, render
from App.models import Influencer_Details, Details_Advertiser
from notifications.signals import notify
from App.Utility import Get_Recipent_User
from .Utility import Get_Ads_Names

# Create your views here.


def Create_Advertisement(request):
    if request.method == "POST":
        Product_Form = Advertisement_Form(request.POST,request.FILES)
        if Product_Form.is_valid():
            Name = Product_Form.cleaned_data["Product_Name"]
            Cost = Product_Form.cleaned_data["Product_Cost"]
            Description = Product_Form.cleaned_data["Product_Description"]
            Img = request.FILES["Product_image"]
            Shipping = Product_Form.cleaned_data["Is_Shipping"]
            User_id = request.user.id
            Adv_Obj = Advertisement_Create(User = User_id,Product_Name =Name, Product_Cost = Cost, Product_Description = Description, Product_image = Img, Is_Shipping = Shipping )
            Adv_Obj.save()
            Recpnt_users = Get_Recipent_User()
            notify.send(request.user,recipient= Recpnt_users, verb= "Created a New Advertisement, Check it Out")
            return redirect("All_Adv")
        else:
            Product_Form = Advertisement_Form()
            return render(request, "CreateADS.html",{"AdvForm":Product_Form,"Error":"Form is not Valid"})
    else:
        Product_Form = Advertisement_Form()
    return render(request, "CreateADS.html",{"AdvForm":Product_Form})
        
def All_Adv(request):
    usid = request.user.id
    try:
        User_Name = Influencer_Details.objects.all().filter(User = usid).values("Slug_Name")[0]["Slug_Name"]
    except:
        User_Name = Details_Advertiser.objects.all().filter(User = usid).values("Adv_Slugname")[0]["Adv_Slugname"]
    if request.method == "POST":
        Ads_frm = Ad_Search(request.POST)
        if Ads_frm.is_valid():
            Search_Input = Ads_frm.cleaned_data["Search"]
            Search_Data = Get_Ads_Names(Ads_Name=Search_Input)
            try:
                Search_Values = Search_Data[1][0] 
            except:
                Search_Values = None
            obj_list =[]
            if Search_Data is not None and Search_Values is not None:
                for i in Search_Data[1][0]:
                    Image = i["Product_image"]
                    Img_Ul = "../../media/{}".format(Image)
                    obj_list.append([i["Product_Name"],i["Product_Cost"],i["Product_Description"],Img_Ul,i["id"]])
                return render(request,"ALL_Adv.html",{"Context_Gig":obj_list,"Profile_Name":User_Name,"Srch_Ad":Ads_frm})
            else:
                Ads_frm =  Ad_Search()
                return redirect("All_Adv")
    else:
        Ads_frm = Ad_Search()
        List = []
        try:
            All_Advs = Advertisement_Create.objects.all().values("Product_Name","Product_Cost","Product_Description", "Product_image","Is_Shipping","id")
            for i in All_Advs:
                Profile_Image = i["Product_image"]
                Img_Url = "../../media/{}".format(Profile_Image)
                List.append([i["Product_Name"],i["Product_Cost"],i["Product_Description"],Img_Url,i["id"]])
            print(List[0])
            return render(request,"ALL_Adv.html",{"Context_Gig":List,"Profile_Name":User_Name ,"Srch_Ad":Ads_frm})
        except:
            return render(request,"ALL_Adv.html",{"Objs":"No Ads are Available","Profile_Name":User_Name,"Srch_Ad":Ads_frm})
    
def Autocomplete(request):
    try:
        Query = request.GET
        Query_Terms = Query.get('term')
        Results = Get_Ads_Names(Ads_Name= Query_Terms)
        if Results is not None:
            Product_Names = Results[0]
            Autocomplete_List = []
            if Product_Names is not None:
                for i in Product_Names:
                    Autocomplete_List.append(i)
                return JsonResponse(Autocomplete_List,safe=False)
    except:
        return JsonResponse([],safe=False)