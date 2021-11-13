from typing import List
from Checkout.models import Project_Creation
from .models import Account, Acount_Influencer, Initial_Data,Influencer_Details,Gig_Attachments
from Offers.models import Earned_by_Freelancer
from Advertiser.models import Advertisement_Create




def Get_Project_Id(Id):
    List =[]

    try:
        Project_Id = Project_Creation.objects.all().filter(Created_For = Id).values("Product_Id","Product_Type","is_Completed")
        if Project_Id is not None:
            for i in range(len(Project_Id)):
                if Project_Id[i]["is_Completed"] == False:
                    List.append([Project_Id[i]["Product_Id"], Project_Id[i]["Product_Type"]])
            
            return List
        else:
            return None
    except:
        return None

def Get_Recipent_User():
    User_Recipent = []
    Id_All = Account.objects.all().values("id")
    for i in range(len(Id_All)):
        User_Recipent.append(Account.objects.get(id = Id_All[i]["id"]))
    return User_Recipent


def Get_Earned_Money(User_Id):
    try:
        List = []
        Dates = []
        Money=[]
        Chart_Data = Earned_by_Freelancer.objects.all().filter(Money_Reciever = User_Id)
        Counter = 0
        for Cht_Data in Chart_Data:
            Dates.append(Counter)
            Money.append(Cht_Data.Value)
            Counter = Counter+1
        return Dates, Money
    except:
        return None


def Get_Spend_Money(User_Id):
    Dates=[]
    Money = []
    try:
        Chart_Data = Earned_by_Freelancer.objects.all().filter(Money_Releser = User_Id)
        Counter = 0
        for Cht_Data in Chart_Data:
            Dates.append(Counter)
            Money.append(Cht_Data.Value)
            Counter = Counter+1
        return Dates, Money
    except:
        return None


def Get_Project_Adv(Id):
    List =[]

    try:
        Project_Id = Project_Creation.objects.all().filter(Created_By = Id).values("Product_Id","Product_Type","is_Completed")
        if Project_Id is not None:
            for i in range(len(Project_Id)):
                if Project_Id[i]["is_Completed"] == False:
                    List.append([Project_Id[i]["Product_Id"], Project_Id[i]["Product_Type"]])
            
            return List
        else:
            return None
    except:
        return None
    

def Search(Value =None):
    if Value is not None:
        if len(Value)>1:
            try:
                Search = Value[0:3]
                return Search
            except:
                return None
        else:
            return None
    else:
        return None
    
def Get_Gig_Names(Gig_Name):
    try:
        List = []
        Product_List = []
        Data_Obj = []
        Search_Value = Search(Value=str(Gig_Name).lower())
        if Search_Value is not None:
            All_Gigs = Initial_Data.objects.all().values("Title")
            for i in All_Gigs:
                List.append(i["Title"])
            
            for j in List:
                String = str(j).lower()
                Found = String.find(Search_Value)
                if Found>-1:
                    Product_List.append(j)
            
            for x in Product_List:
                Data = Initial_Data.objects.all().filter(Title = x).values("Title","Category_Service","Descriptions","id")
                Data_Obj.append(Data)
                    
            return Product_List, Data_Obj
        else:
            return None
    except:
        return None
        
        
def Get_Influencer():
    List_inf = []
    try:
        Ids = Acount_Influencer.objects.all().filter(Is_Influencer = True).values("User")
        for i in Ids:
            us = Account.objects.all().filter(id=i["User"]).values("username")[0]["username"]
            Slg = Influencer_Details.objects.all().filter(User = i["User"]).values("Slug_Name")[0]["Slug_Name"]
            Slg_id = i["User"]
            prof_url = "{}_{}".format(Slg_id, Slg)
            List_inf.append([us,prof_url])
        return List_inf[0:4]
    except:
        return None
    
def Get_Influencers_by_Search(Inf_Name):
    try:
        List = []
        Product_List = []
        Data_Obj = []
        Search_Value = Search(Value=str(Inf_Name).lower())
        if Search_Value is not None:
            All_Inf = Influencer_Details.objects.all().values("Slug_Name")
            for i in All_Inf:
                List.append(i["Slug_Name"])
            
            for j in List:
                String = str(j).lower()
                Found = String.find(Search_Value)
                if Found>-1:
                    Product_List.append(j)
            
            for x in Product_List:
                Data = Influencer_Details.objects.all().filter(Slug_Name = x).values("Profile_Picture","Descriptions","Country","User")
                Data_Obj.append(Data)
                    
            return Product_List, Data_Obj
        else:
            return None
    except:
        return None
    
    
def Get_Advertisements():
    try:
        List_Ads = []
        All_Gigs = Advertisement_Create.objects.all().values("Product_Name")
        for i in All_Gigs:
            List_Ads.append(i["Product_Name"])
        return List_Ads[0:4]
    except:
        return None
        
def Get_Gigs():
    try:
        Gigs_Data = Initial_Data.objects.all().values("Title","id")
        Attachment_Url = "../../media/Thunbnail/glass_Full.png"
        for i in Gigs_Data:
            try:
                Urls = Gig_Attachments.objects.all().filter(Gig_Id = i["id"]).values("Work_Thumbnails")[0]["Work_Thumbnails"]
            except:
                Urls =None
            if Urls is not None:
                Profile_Url = "../../media/{}".format(Urls)
                i["image"] = Profile_Url
            else:
                i["image"] = Attachment_Url
        return Gigs_Data[0:4]
    except:
        return None
    
            
        