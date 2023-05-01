// ignore_for_file: library_private_types_in_public_api

import 'dart:convert';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<Map<String, dynamic>> data = [];

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    final response =
        await http.get(Uri.parse('http://127.0.0.1:5000/attendance_student'));

    if (response.statusCode == 200) {
      final jsonList = jsonDecode(response.body) as List<dynamic>;
      setState(() {
        data = jsonList.cast<Map<String, dynamic>>().toList();
      });
    } else {
      throw Exception('Failed to load data from API');
    }
  }

  Future<void> sendEmail(String recipientEmail) async {
    final String emailUrl =
        'mailto:$recipientEmail?subject=Attendance Update&body=Hello, \n\n';
    // ignore: deprecated_member_use
    if (await canLaunch(emailUrl)) {
      // ignore: deprecated_member_use
      await launch(emailUrl);
    } else {
      throw 'Could not launch $emailUrl';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Class Attendance'),
      ),
      body: ListView.builder(
        itemBuilder: (BuildContext context, int index) {
          final student = data[index]['Student'];
          final attendance = data[index]['Attendance'];
          return ListTile(
            title: Text('${student['first_name']} ${student['last_name']}'),
            subtitle: Text('Status: ${attendance['status']}'),
            trailing: IconButton(
              icon: const Icon(Icons.email),
              onPressed: () => sendEmail(student['email']),
            ),
            //trailing: Text(student['email']),
          );
        },
        itemCount: data.length,
      ),
    );
  }
}
