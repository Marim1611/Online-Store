import 'package:flutter/material.dart';

class SubmitOrder extends StatefulWidget {
  @override
  _SubmitOrderState createState() => _SubmitOrderState();
}

class _SubmitOrderState extends State<SubmitOrder> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.teal,
        title: Text('Order Submission ',
        ),
        centerTitle: true,
        actions: <Widget>[

        ],
      ),



    );
  }
}
