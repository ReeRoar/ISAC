// ignore_for_file: file_names, library_private_types_in_public_api, camel_case_types, duplicate_ignore

import 'package:flutter/material.dart';
import 'GetStudents.dart';

// ignore: camel_case_types
class student_List extends StatefulWidget {
  const student_List({super.key});

  @override
  _student_ListState createState() => _student_ListState();
}

class _student_ListState extends State<student_List> {
  List<String> _studentNames = [];

  @override
  void initState() {
    super.initState();
    _fetchStudentNames();
  }

  Future<void> _fetchStudentNames() async {
    try {
      final studentNames = await GetStudents.getStudentNames();
      //debugPrint(studentNames);
      setState(() {
        _studentNames = studentNames;
      });
    } catch (e) {
      // handle error
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Student List'),
      ),
      body: _studentNames.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _studentNames.length,
              itemBuilder: (BuildContext context, int index) {
                final studentName = _studentNames[index];
                return ListTile(
                  title: Text(studentName),
                );
              },
            ),
    );
  }
}
