import 'dart:convert';
import 'dart:developer';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter_mail_send/screens/signup_model.dart';

Future<http.Response?> register(SignUpBody data) async {
  http.Response? response;
  try {
    response = await http.post(Uri.parse("http://127.0.0.1:5000/login"),
        headers: {
          HttpHeaders.contentTypeHeader: "login/json",
        },
        body: jsonEncode(data.toJson()));
  } catch (e) {
    log(e.toString());
  }
  return response;
}
