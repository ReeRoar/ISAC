// ignore_for_file: prefer_const_constructors, prefer_interpolation_to_compose_strings, avoid_print, deprecated_member_use, camel_case_types, duplicate_ignore, unused_import

import 'package:flutter/material.dart';
import 'package:flutter_email_sender/flutter_email_sender.dart';
import 'package:flutter_mail_send/screens/home.dart';
import 'package:mailer/mailer.dart';
import 'package:mailer/smtp_server.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'screens/home.dart';

void main() {
  runApp(myApp()); //it was myApp :: the code after is added
}

class myApp extends StatelessWidget {
  const myApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: HomePage(),
    );
  }
}
