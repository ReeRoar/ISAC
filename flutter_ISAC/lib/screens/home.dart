// ignore_for_file: prefer_const_constructors, duplicate_ignore

import 'package:flutter/material.dart';
import 'package:flutter_mail_send/screens/sendemail.dart';
//ignore: implementation_imports
//import 'package:flutter/src/widgets/container.dart';
//import 'package:flutter/src/widgets/framework.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  get style => null;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        // ignore: duplicate_ignore
        appBar: AppBar(
          // ignore: prefer_const_constructors
          title: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children:
                  // ignore: prefer_const_literals_to_create_immutables
                  [
                Text(
                  "University of Hartford",
                  style: TextStyle(
                      fontSize: 14.0,
                      color: Color.fromARGB(255, 245, 2, 2),
                      fontFamily: 'Roboto'),
                ),
                Text(
                  'Class Attendance',
                  style: TextStyle(color: Colors.white, fontSize: 20),
                ),
              ]),
        ),
        floatingActionButton: FloatingActionButton.extended(
          onPressed: navigateToSendEmailPage,
          backgroundColor: Color.fromARGB(255, 245, 246, 246),
          label: Text(
            'Select Absent Student',
            style: TextStyle(color: Colors.red),
          ),
        ),
        body: ListView());
  }

  void navigateToSendEmailPage() {
    final route = MaterialPageRoute(
      builder: (context) => SendEmailPage(),
    );
    Navigator.push(context, route);
  }
}
