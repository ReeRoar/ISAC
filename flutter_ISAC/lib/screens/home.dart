import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  // ignore: library_private_types_in_public_api
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<Map<String, dynamic>> data = [];
  Map<String, dynamic> attendanceCount = {};

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    final studentResponse =
        await http.get(Uri.parse('http://127.0.0.1:5000/attendance_student'));
    final countResponse =
        await http.get(Uri.parse('http://127.0.0.1:5000/attendance_count'));

    if (studentResponse.statusCode == 200 && countResponse.statusCode == 200) {
      final jsonList = jsonDecode(studentResponse.body) as List<dynamic>;
      setState(() {
        data = jsonList.cast<Map<String, dynamic>>().toList();
        attendanceCount = jsonDecode(countResponse.body) as Map<String, dynamic>;
      });
    } else {
      throw Exception('Failed to load data from API');
    }
  }

  Future<void> updateAttendanceCount() async {
    final response =
        await http.get(Uri.parse('http://127.0.0.1:5000/attendance_count'));

    if (response.statusCode == 200) {
      setState(() {
        attendanceCount = jsonDecode(response.body) as Map<String, dynamic>;
      });
    } else {
      throw Exception('Failed to load attendance count data from API');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ECE472 Class Attendance'),
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
      bottomNavigationBar: BottomAppBar(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Total Students: ${attendanceCount['student_count'] ?? 'Unknown'}'),
              Text('Camera: ${attendanceCount['camera_value']}, RFID: ${attendanceCount['rfid_value']}, Mismatch Counter: ${attendanceCount['mismatch_counter']}'),
              ElevatedButton(
                onPressed: updateAttendanceCount,
                child: const Text('Update'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}


/*
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
*/