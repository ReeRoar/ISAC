// ignore_for_file: prefer_const_constructors, prefer_interpolation_to_compose_strings, avoid_print, deprecated_member_use, camel_case_types, duplicate_ignore, unused_import

import 'package:flutter/material.dart';
import 'package:flutter_email_sender/flutter_email_sender.dart';
import 'package:flutter_mail_send/screens/data_class.dart';
import 'package:flutter_mail_send/screens/home.dart';
import 'package:flutter_mail_send/screens/sign_up.dart';
import 'package:mailer/mailer.dart';
import 'package:mailer/smtp_server.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
// ignore: duplicate_import
import 'screens/sign_up.dart';

void main() {
  //runApp(myApp()); //it was myApp :: the code after is added
  runApp(MultiProvider(providers: [
    ChangeNotifierProvider(create: (_) => DataClass()),
  ], child: const myApp()));
}

class myApp extends StatelessWidget {
  const myApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      //home: HomePage(),
      home: const ProviderDemoScreen(),
    );
  }
}

//this class was added

class ProviderDemoScreen extends StatefulWidget {
  const ProviderDemoScreen({Key? key}) : super(key: key);

  @override
  // ignore: library_private_types_in_public_api
  _ProviderDemoScreenState createState() => _ProviderDemoScreenState();
}

class _ProviderDemoScreenState extends State<ProviderDemoScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300],
      appBar: AppBar(
        title: const Text("ISAC"),
      ),
      body: Center(
        child: GestureDetector(
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => SignUpPage()),
            );
          },
          child: Center(
            child: Container(
              height: 70,
              padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 20),
              margin: const EdgeInsets.only(left: 40, right: 40),
              decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(15),
                  boxShadow: const [
                    BoxShadow(
                      color: Colors.grey,
                      offset: Offset(4, 4),
                      blurRadius: 15,
                      spreadRadius: 1,
                    ),
                    BoxShadow(
                      color: Colors.red,
                      offset: Offset(-4, -4),
                      blurRadius: 15,
                      spreadRadius: 1,
                    ),
                  ]),
              child: const Text(
                "Go to Singup page",
                style: TextStyle(
                  fontSize: 20,
                  color: Color.fromARGB(255, 108, 131, 146),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
