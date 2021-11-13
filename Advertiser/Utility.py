from .models import Advertisement_Create

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
    
def Get_Ads_Names(Ads_Name):
    try:
        List = []
        Product_List = []
        Data_Obj = []
        Search_Value = Search(Value=str(Ads_Name).lower())
        if Search_Value is not None:
            All_Gigs = Advertisement_Create.objects.all().values("Product_Name")
            for i in All_Gigs:
                List.append(i["Product_Name"])
            
            for j in List:
                String = str(j).lower()
                Found = String.find(Search_Value)
                if Found>-1:
                    Product_List.append(j)
            
            for x in Product_List:
                Data = Advertisement_Create.objects.all().filter(Product_Name = x).values("Product_Name","Product_Cost","Product_Description", "Product_image","Is_Shipping","id")
                Data_Obj.append(Data)
                    
            return Product_List, Data_Obj
        else:
            return None
    except:
        return None