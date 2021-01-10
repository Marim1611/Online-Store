import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'customer_views/product.dart';
import 'customer_views/calss_category.dart';
import 'customer_views/addcartClass.dart';
import 'customer_views/cart.dart';
import 'customer_views/calss_order.dart';
import 'customer_views/category_page.dart';
//don't forget to include in the pubspec.yaml: http: ^0.12.0+2

class URLS {
  //This stores the url that we'll deal with the restful api through
  //for web-based applications this will be http://localhost:5000/
  //for mobile-based applications (emulators) this will be http://10.0.2.2:5000
  static const String BASE_URL = 'http://10.0.2.2:5000';
}
///*************************************MARIM NASER ********************************************************************

/// Best Sellers
Future <dynamic> GetBestSellerProducts() async{
  final response = await http.get ('${URLS.BASE_URL}/BestproductsHome');

  if(response.statusCode ==200){
    List jsonResponse=json.decode(response.body);
    return jsonResponse.map((product) =>new Product.fromJson(product)).toList();
  }
  else{
    throw Exception("Failed To load Best Seller Products from API");
  }
}
/// offers
Future <dynamic> GetProductsWithOffers() async{
  final response = await http.get ('${URLS.BASE_URL}/OffersHome');

  if(response.statusCode ==200){
    List jsonResponse=json.decode(response.body);
    return jsonResponse.map((product) =>new Product.fromJson(product)).toList();
  }
  else{
    throw Exception("Failed To load Best Seller Products from API");
  }
}
/// Categories
Future <dynamic> GetCategories() async{
  final response = await http.get ('${URLS.BASE_URL}/Categories');

  if(response.statusCode ==200){
    List jsonResponse=json.decode(response.body);
    return jsonResponse.map((product) =>new MyCategory.fromJson(product)).toList();
  }
  else{
    throw Exception("Failed To load Categories from API");
  }
}

/// products of category
Future<dynamic> CategoryProducts(int CID) async{

  print('$CID');
  Map <String,dynamic> CAT_ID= {"CID":'$CID'};
  final response = await http.post('${URLS.BASE_URL}/CategoryProducts', body:CAT_ID );
  if (response.statusCode == 200) {

    List jsonResponse=json.decode(response.body);
    return jsonResponse.map((product) =>new Product.fromJson(product)).toList();

    return json.decode(response.body);
  }
  else{
    throw Exception("Failed To load Categories from API");
  }
}
///Add To Cart
Future<dynamic> AddToCart(int CustomerID, int productID, int qty) async{
  Map <String,dynamic> addingtocart ={
    'proID': productID.toString(),
    'custID': CustomerID.toString(),
    'QTY':qty.toString()
  };
  print(productID.toString()+" "+CustomerID.toString());
  final response = await http.post('${URLS.BASE_URL}/addtocart', body: addingtocart );
  print("noran");
  if (response.statusCode == 200) {
    print("yarab");
    return json.decode(response.body);
  }
  else{
    print("EXEPTION");
    throw Exception("Failed To load Categories from API");
  }
}
/// get all products in the cart
Future<dynamic> GetCartProducts(int CID) async{

  print('$CID');
  Map <String,dynamic> CAT_ID= {"CID":'$CID'};
  final response = await http.post('${URLS.BASE_URL}/getCart', body:CAT_ID );
  if (response.statusCode == 200) {

    List jsonResponse=json.decode(response.body);
    return jsonResponse.map((product) =>new Product.fromJson(product)).toList();

    return json.decode(response.body);
  }
  else{
    throw Exception("Failed To load Categories from API");
  }
}
/// increment quantity
Future<dynamic> inc_qty(int CustomerID, int productID) async{
  Map <String,dynamic> inc_id = {
    'proID': productID.toString(),
    'custID': CustomerID.toString(),
  };
  final response = await http.post('${URLS.BASE_URL}/incQTY', body: inc_id );
  if (response.statusCode == 200) {
    return json.decode(response.body);
  }
  else{
    print("EXEPTION");
    throw Exception("Failed To load Categories from API");
  }
}
/// deccrement quantity
Future<dynamic> dec_qty(int CustomerID, int productID) async{
  Map <String,dynamic> dec_id = {
    'proID': productID.toString(),
    'custID': CustomerID.toString(),
  };
  print("TB EHHHH");
  final response = await http.post('${URLS.BASE_URL}/decQTY', body: dec_id );
  if (response.statusCode == 200) {
    return json.decode(response.body);
  }
  else{
    throw Exception("Failed To load Categories from API");
  }
}
/// get aty of certain product
Future<dynamic> GetQTY(int PROID) async {

  print('$PROID');
  Map <String, dynamic> CAT_ID = {"proID": '$PROID'};

  final response = await http.post('${URLS.BASE_URL}/getCart', body: CAT_ID);
  if (response.statusCode == 200) {
    List jsonResponse = json.decode(response.body);
    return jsonResponse.map((product) => new Product.fromJson(product))
        .toList();

    return json.decode(response.body);
  }
  else {
    throw Exception("Failed To load Categories from API");
  }
}
/// delete product from cart
Future<dynamic> DeleteFromCart(int CustomerID, int productID) async{
  Map <String,dynamic> delete_cart = {
    'proID': productID.toString(),
    'custID': CustomerID.toString(),
  };
  final response = await http.post('${URLS.BASE_URL}/deletefromcart', body:delete_cart );
  if (response.statusCode == 200) {
    return json.decode(response.body);
  }
  else{
    print("EXEPTION");
    throw Exception("Failed To load Categories from API");
  }
}
///making order
/// 1-get price and qty of products in cart
Future<dynamic> GetTotalPayment(int CID) async{

  Map <String,dynamic> CAT_ID= {"CID":'$CID'};

  final response = await http.post('${URLS.BASE_URL}/priceQTYget', body:CAT_ID );
  if (response.statusCode == 200) {

    List jsonResponse=json.decode(response.body);
    return jsonResponse.map((product) =>new TotalPayement.fromJson(product)).toList();
  }
  else{

    throw Exception("Failed To load Categories from API");
  }
}
///2- insert new order
Future<dynamic> MakeOrder(int CustomerID, int totalpay) async{
  Map <String,dynamic> makeneworder ={
    'custID': CustomerID.toString(),
    'totpay':totalpay.toString(),
  };
  print(CustomerID.toString() + totalpay.toString() );
  final response = await http.post('${URLS.BASE_URL}/makeorder', body:makeneworder );

  print("noran");
  if (response.statusCode == 200) {
    print("yarab");
    return json.decode(response.body);
  }
  else{
    print("EXEPTION");
    throw Exception("Failed To insert order into API");
  }
}
///3- Clear The Cart Fot this customer ONLY
Future<dynamic> ClearCart(int cID) async{
  ///customer ID
  Map <String,dynamic> clearmycart= {"CID":cID.toString()};
  print("TB EHHHH2");
  final response = await http.post('${URLS.BASE_URL}/emptycart', body:clearmycart );
  print("noran2");
  if (response.statusCode == 200) {
    print("yarab2");
    return json.decode(response.body);
  }
  else{
    print("EXEPTION");
    throw Exception("Failed To load Categories from API");
  }
}
/// get my orders
Future<dynamic> GetMyOrders(int CID) async{


  Map <String,dynamic> CAT_ID= {"CID":'$CID'};
  print(CID.toString());
  final response = await http.post('${URLS.BASE_URL}/getorder', body:CAT_ID );
  if (response.statusCode == 200) {
    print("hello");
    List jsonResponse = json.decode(response.body);
    return jsonResponse.map((order) => new OrderM.fromJson(order)).toList();
  }
  else{
    print("helloxx");
    throw Exception("Failed To load orders from API");
  }
}
/// Feedback Delivery man
Future<dynamic> FeedbackDM( double myrate, String message,int CustomerID, int DMID) async{
  Map <String,dynamic> feedbackdmm ={
    'myrate':myrate.toString(),
    'MSG': message,
    'custID': CustomerID.toString(),
    'dmID':DMID.toString()
  };
  print(myrate.toString()+ message+CustomerID.toString()+" "+DMID.toString());
  print(feedbackdmm);
  final response = await http.post('${URLS.BASE_URL}/feedbackdm', body:feedbackdmm );
  print("noran");
  if (response.statusCode == 200) {
    print("yarab");
    return json.decode(response.body);


  }
  else{
    print("EXEPTION");
    throw Exception("Failed To insert feedback into API");
  }
}
///comment product
Future<dynamic> Commentpro(int CustomerID , String Msg,int proid) async{

  print(CustomerID.toString());

  Map <String,dynamic> commment ={
    'MSG':Msg,
    'custID': CustomerID.toString(),
    'proID':proid.toString()

  };
  final response = await http.post('${URLS.BASE_URL}/commentproduct', body:commment );
  print("hyy");
  if (response.statusCode == 200) {
    return json.decode(response.body);
  }
  else{
    print("yoooo");
    throw Exception("Failed To load Categories from API");
  }
}
/// show comments on certain product
Future<dynamic> showcomment(int proID) async{

  print('$proID');
  Map <String,dynamic> CAT_ID= {"PROID":'$proID'};
  final response = await http.post('${URLS.BASE_URL}/showcommentproduct', body:CAT_ID );
  if (response.statusCode == 200) {

    print(response.body);
    dynamic jsonResponse=json.decode(response.body);
    print(jsonResponse);
    print(jsonResponse.length);
    print(jsonResponse[0]);
   ///return jsonResponse.map((product) =>new String.fromJson(product)).toList();

     return jsonResponse;
   ///  return json.decode(json.decode(response.body));
  }
  else{
    throw Exception("Failed To load Categories from API");
  }
}
///rate  product
Future<dynamic> Ratepro(int CustomerID , double rate,int proid) async{

  print(CustomerID.toString());
  print(proid.toString());
  print(rate.toString());


  Map <String,dynamic> commment ={
    'myrate':rate.toString(),
    'custID': CustomerID.toString(),
    'proID':proid.toString()

  };

  final response = await http.post('${URLS.BASE_URL}/rateproduct', body:commment );
  print("hyy");
  if (response.statusCode == 200) {
    return json.decode(response.body);
    print("hyy");
  }
  else{
    print("yoooo");
    throw Exception("Failed To load Categories from API");
  }
}
/// show rate of certain product
Future<dynamic> showrate(int proID) async{
  Map <String,dynamic> CAT_ID= {"PROID":'$proID'};
  print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh");
  print(CAT_ID);
  final response = await http.post('${URLS.BASE_URL}/showrateproduct', body:CAT_ID );
  if (response.statusCode == 200) {
    print("HHHHHHHHHHHHHHHHHH");
    print(response.body);
    dynamic jsonResponse= json.decode(response.body);
    print(jsonResponse[0][0]);
    ///print(jsonResponse.length);
    ///print(jsonResponse[0]);
    return jsonResponse[0][0];
  }
  else{
    print("exhhxx");
    throw Exception("Failed To load Categories from API");
  }
}
///Make Complaint
Future<dynamic> MakeComplaints(int CustomerID , String Msg) async{

  print(CustomerID.toString());

  Map <String,dynamic> makeComplaint ={
    'custID': CustomerID.toString(),
    'MSG':Msg
  };
  final response = await http.post('${URLS.BASE_URL}/complaint', body: makeComplaint );
  print("hyy");
  if (response.statusCode == 200) {
    return json.decode(response.body);
  }
  else{
    print("yoooo");
    throw Exception("Failed To load Categories from API");
  }
}




