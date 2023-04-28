//this class is a model of the Api

// ignore_for_file: file_names
import 'dart:convert';
import 'package:http/http.dart' as http;

class GetStudents {
  static Future<List<String>> getStudentNames() async {
    final response =
        await http.get(Uri.parse('http://127.0.0.1:5000/students'));

    if (response.statusCode == 200) {
      final studentsJson = json.decode(response.body) as List<dynamic>;
      final List<String> studentNames = studentsJson
          .map((student) => student['last_name'] as String)
          .toList();
      return studentNames;
    } else {
      throw Exception('Failed to load students');
    }
  }
}

/*class GetStudents {
  String? firstName;
  String? lastName;
  String? email;

  GetStudents({this.firstName, this.lastName, this.email});

  GetStudents.fromJson(Map<String, dynamic> json) {
    firstName = json['first name'];
    lastName = json['last name'];
    email = json['email'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['first name'] = firstName;
    data['last name'] = lastName;
    data['email'] = email;
    return data;
  }
}

/*class student {
  final String name; 
  final String email; 


const student (student{
 required this.name, 
 required this.email,
}); 

static student fromJson(json) => student(
  name: json['Student name'], 
  email: json['email'], 

); 
} 
*/
*/