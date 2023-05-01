//this class is a model of the Api
//converts from JSON to Dart
// ignore_for_file: file_names, unused_import, unnecessary_this
import 'dart:convert';
import 'package:http/http.dart' as http;

//the new code

class GetStudents {
  Attendance? attendance;
  //Course? course;
  Student? student;

  GetStudents({this.attendance, this.student});

  //GetStudents({this.attendance, this.course, this.student});

  GetStudents.fromJson(Map<String, dynamic> json, attendance) {
    attendance = json['Attendance'] != null
        ? Attendance.fromJson(json['Attendance'])
        : null;
    //course = json['Course'] != null ? Course.fromJson(json['Course']) : null;
    student =
        json['Student'] != null ? Student.fromJson(json['Student']) : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    if (this.attendance != null) {
      data['Attendance'] = this.attendance!.toJson();
    }
    /*
    if (this.course != null) {
      data['Course'] = this.course!.toJson();
    }
    */
    if (this.student != null) {
      data['Student'] = this.student!.toJson();
    }
    return data;
  }
}

class Attendance {
  int? courseNumber;
  String? date;
  int? id;
  String? status;
  int? studentId;

  Attendance(
      {this.courseNumber, this.date, this.id, this.status, this.studentId});

  Attendance.fromJson(Map<String, dynamic> json) {
    courseNumber = json['course_number'];
    date = json['date'];
    //id = json['id'];
    status = json['status'];
    //studentId = json['student_id'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['course_number'] = this.courseNumber;
    data['date'] = this.date;
    // data['id'] = this.id;
    data['status'] = this.status;
    //data['student_id'] = this.studentId;
    return data;
  }
}

class Student {
  String? email;
  String? firstName;
  String? lastName;
  int? studentId;

  Student({this.email, this.firstName, this.lastName, this.studentId});

  Student.fromJson(Map<String, dynamic> json) {
    email = json['email'];
    firstName = json['first_name'];
    lastName = json['last_name'];
    studentId = json['student_id'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['email'] = this.email;
    data['first_name'] = this.firstName;
    data['last_name'] = this.lastName;
    data['student_id'] = this.studentId;
    return data;
  }
}

/*
class Course {
  int? courseNumber;
  String? endTime;
  String? startTime;

  Course({this.courseNumber, this.endTime, this.startTime});

  Course.fromJson(Map<String, dynamic> json) {
    courseNumber = json['course_number'];
    endTime = json['end_time'];
    startTime = json['start_time'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['course_number'] = this.courseNumber;
    data['end_time'] = this.endTime;
    data['start_time'] = this.startTime;
    return data;
  }
}
*/

//this code is the last one whhere it loads the students names to a list view to be used
//in the stduent_list.dart
/*class GetStudents {
  static Future<List<String>> getStudentNames() async {
    final response =
        await http.get(Uri.parse('http://127.0.0.1:5000/attendance_student'));
        print(response.body); 
  
}


//this code is the last one whhere it loads the students names to a list view to be used 
//in the stduent_list.dart 
/ if (response.statusCode == 200) {
      final studentsJson = json.decode(response.body) as List<dynamic>;
      final List<String> studentNames = studentsJson
          .map((student) => student['last_name'] as String)
          .toList();
      return studentNames;
    } else {
      throw Exception('Failed to load students');
    }
  } */
