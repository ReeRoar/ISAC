import 'dart:async';
// ignore: avoid_web_libraries_in_flutter
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
// ignore: unused_import
import 'package:http/http.dart' as http;

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
    try {
      final dio = Dio();
      final response =
          await dio.get('http://127.0.0.1:5000/attendance_student');

      if (response.statusCode == 200) {
        final jsonList = response.data as List<dynamic>;
        setState(() {
          data = jsonList.cast<Map<String, dynamic>>().toList();
        });
      } else {
        throw Exception('Failed to load data from API');
      }
    } catch (error) {
      throw Exception('Failed to load data from API');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: ListView.builder(
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
    );
  }
}
