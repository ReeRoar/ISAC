// ignore_for_file: prefer_const_constructors, unnecessary_import

import 'package:flutter/material.dart';
// ignore: implementation_imports
import 'package:flutter/src/widgets/framework.dart';
// ignore: implementation_imports
import 'package:flutter/src/widgets/basic.dart';
import 'package:url_launcher/url_launcher.dart';

class SendEmailPage extends StatefulWidget {
  const SendEmailPage({super.key});

  @override
  State<SendEmailPage> createState() => _SendEmailPageState();
}

// ignore: non_constant_identifier_names
SendEmail() {
  final Uri emailLaunchUri = Uri(
      scheme: 'mailto',
      path: 'Absent Student Email@hartford.edu',
      queryParameters: {
        'subject': 'You have missed a class!',
        'body':
            'Hello! your professor would like to notify you that you have missed a class',
      });

  launchUrl(emailLaunchUri);
}

class _SendEmailPageState extends State<SendEmailPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(
            'Notify Students',
            style: TextStyle(color: Colors.red, fontSize: 20),
          ),
        ),
        body: Center(
            child: TextButton(
          onPressed: SendEmail(),
          child: Text('Send an Email',
              style: TextStyle(color: Colors.red, fontSize: 7)),
        )));
  }

  /*SendEmail() {
    final Uri emailLaunchUri = Uri(
        scheme: 'mailto',
        path: 'Absent Student Email@hartford.edu',
        queryParameters: {
          'subject': 'You have missed a class!',
          'body':
              'Hello! your professor would like to notify you that you have missed a class',
        });

    launchUrl(emailLaunchUri);
  }
  */
}
