import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

//this class works perfectly

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  // ignore: library_private_types_in_public_api
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('CSE472 Class Attendance'),
      ),
      body: RefreshIndicator(
        onRefresh: loadData,
        child: ListView.builder(
          itemBuilder: (BuildContext context, int index) {
            final student = data[index]['Student'];
            final attendance = data[index]['Attendance'];
            return ListTile(
              title: Text('${student['first_name']} ${student['last_name']}'),
              subtitle: Text('Status: ${attendance['status']}'),
              trailing: Text(student['email']),
            );
          },
          itemCount: data.length,
        ),
      ),
    );
  }
}
