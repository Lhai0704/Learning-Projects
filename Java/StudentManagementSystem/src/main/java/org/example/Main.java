package org.example;

import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<User> users = new ArrayList<>();
        loop:
        while (true) {
            System.out.println("Welcome to the Student Management System");
            System.out.println("select: 1 login 2 register 3 forget password");
            switch (sc.nextInt()) {
                case 1 -> {
                    if (login(users)) {
                        break loop;
                    }
                }
                case 2 -> register(users);
                case 3 -> forgetPassword(users);
                default -> System.out.println("illegal input. ");
            }
        }


        ArrayList<Student> students = new ArrayList<>();

        while (true) {
            System.out.println("Welcome to the Student Management System");
            System.out.println("1: add student");
            System.out.println("2: remove student");
            System.out.println("3: modify student");
            System.out.println("4: select student");
            System.out.println("5: quit");
            System.out.print("enter:");
            int menu = sc.nextInt();
            switch (menu) {
                case 1 ->       // add
                        addStudent(students);
                case 2 -> {     // remove
                    System.out.print("enter student id:");
                    int index = findById(students, sc.next());
                    removeStudent(students, index);
                }
                case 3 ->       // modify
                        modifyStudent(students);
                case 4 -> {     // select
                    if (students.size() == 0) {
                        System.out.println("no student info. ");
                    } else {
                        System.out.println("id     name     age     address");
                        for (Student student : students) {
                            System.out.println(student.getId() + "    " + student.getName() + "    " + student.getAge()
                                    + "    " + student.getAddress());
                        }
                    }
                }
                case 5 -> {
                    return;
                }
                default -> System.out.println("illegal input. enter again");
            }

        }
    }


    public static int findById(ArrayList<Student> arr, String id) {
        for (int i = 0; i <= arr.size() - 1; i++) {
            if (arr.get(i).getId().equals(id)) {
                return i;
            }
        }
        return -1;

    }


    public static void addStudent(ArrayList<Student> students) {
        Scanner sc = new Scanner(System.in);
        Student student = new Student();
        System.out.println("enter student id:");
        String id = sc.next();
        if (findById(students, id) == -1) {
            student.setId(id);
            System.out.println("enter student name:");
            student.setName(sc.next());
            System.out.println("enter student age:");
            student.setAge(sc.nextInt());
            System.out.println("enter student address:");
            student.setAddress(sc.next());
            students.add(student);
        } else {
            System.out.println("student id is already exist. ");
        }
    }


    public static void removeStudent(ArrayList<Student> students, int index) {
        if (index >= 0) {
            students.remove(index);
            System.out.println("remove successful. ");
        } else {
            System.out.println("id not exist. ");
        }
    }


    public static void modifyStudent(ArrayList<Student> students) {
        Scanner sc = new Scanner(System.in);
        System.out.print("enter student id:");
        int index = findById(students, sc.next());
        if (index >= 0) {
            System.out.println("enter student name:");
            students.get(index).setName(sc.next());
            System.out.println("enter student age:");
            students.get(index).setAge(sc.nextInt());
            System.out.println("enter student address:");
            students.get(index).setAddress(sc.next());
            System.out.println("modify successful. ");
        } else {
            System.out.println("id not exist. ");
        }
    }


    public static int findUser(ArrayList<User> users, String name) {
        for (int i = 0; i <= users.size() - 1; i++) {
            if (users.get(i).getName().equals(name)) {
                return i;
            }
        }
        return -1;
    }


    // unique, 3-15, numbers+character
    public static boolean checkName(ArrayList<User> users, String name) {
        if (name.length() < 3 || name.length() > 15) {
            System.out.println("name length illegal. ");
            return false;
        }

        // numbers+character
        boolean number = false;
        boolean character = false;
        char c;
        for (int i = 0; i <= name.length() - 1; i++) {
            c = name.charAt(i);
            if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
                character = true;
            }
            if (c >= '0' && c <= '9') {
                number = true;
            }
            if (number && character) {
                break;
            }
        }
        if (!number || !character) {
            System.out.println("numbers+character illegal");
            return false;
        }

        if (findUser(users, name) != -1) {
            System.out.println("name is not unique. ");
            return false;
        }

        return true;
    }


    public static boolean checkIdCard(String idCard) {
        if (idCard.length() != 18) {
            System.out.println("name length illegal. ");
            return false;
        }

        if (idCard.charAt(0) == '0') {
            System.out.println("start with 0. ");
            return false;
        }

        for (int i = 0; i <= 16; i++) {
            char c = idCard.charAt(i);
            if (c < '0' || c > '9') {
                System.out.println("begin 17 have character. ");
                return false;
            }
        }

        char last = idCard.charAt(17);
        if ((last >= '0' && last <= '9') || last == 'x' || last == 'X') {
            return true;
        } else {
            System.out.println("last character illegal. ");
            return false;
        }
    }


    public static boolean checkPhone(String phone) {
        if (phone.length() != 11 || phone.charAt(0) == '0') {
            return false;
        }
        for (int i = 0; i <= phone.length() - 1; i++) {
            char c = phone.charAt(i);
            if (c < '0' || c > '9') {
                return false;
            }
        }
        return true;
    }


    public static boolean checkNameExist(ArrayList<User> users, String name) {
        for (int i = 0; i <= users.size() - 1; i++) {
            if (users.get(i).getName().equals(name)) {
                return true;
            }
        }
        return false;
    }


    public static String verificationCode(int length) {
        char[] arr = new char[length];
        Random r = new Random();
        for (int i = 0; i <= length - 2; i++) {
            int randomCharacter = r.nextInt(52);
            if (randomCharacter <= 25) {
                arr[i] = (char) (randomCharacter + 97);
            } else {
                arr[i] = (char) (randomCharacter + 39);
            }
        }
        arr[length - 1] = (char) (r.nextInt(9) + 49);

        for (int i = 0; i <= length - 1; i++) {
            int index = r.nextInt(length - 1);
            char temp = arr[i];
            arr[i] = arr[index];
            arr[index] = temp;
        }
        return new String(arr);
    }


    public static boolean checkPassword(ArrayList<User> users, String name, String password) {
        for (int i = 0; i <= users.size() - 1; i++) {
            User user = users.get(i);
            if (user.getName().equals(name) && user.getPassword().equals(password)) {
                return true;
            }
        }
        return false;
    }


    public static boolean login(ArrayList<User> users) {
        Scanner sc = new Scanner(System.in);
        String name;
        // username
        while (true) {
            System.out.print("enter username:");
            name = sc.next();
            if (checkNameExist(users, name)) {
                break;
            } else {
                System.out.println("username is not exist, register first. ");
                return false;
            }
        }

        int passwordCount = 0;
        // password
        loop:
        while (true) {
            System.out.print("enter your password: ");
            String password = sc.next();
            passwordCount++;

            while (true) {
                System.out.print("enter verification code: ");
                String code = verificationCode(5);
                System.out.println(code);
                String inputCode = sc.next();
                if (inputCode.equals(code)) {
                    if (checkPassword(users, name, password)) {
                        break loop;
                    } else if (passwordCount < 3) {
                        System.out.println("wrong password, " + (3 - passwordCount) + " times left. ");
                        break;
                    } else {
                        System.out.println("three wrong password. ");
                        return false;
                    }
                } else {
                    System.out.println("wrong verification code, ");
                }
            }
        }
        return true;
    }


    public static void register(ArrayList<User> users) {
        Scanner sc = new Scanner(System.in);
        User user = new User();
        // name
        while (true) {
            System.out.println("enter name: (unique, 3-15, numbers+character)");
            String name = sc.next();
            if (checkName(users, name)) {
                user.setName(name);
                break;
            } else {
                System.out.println("name illegal, enter again. ");
            }
        }

        // password
        while (true) {
            System.out.print("enter your password: ");
            String password1 = sc.next();
            System.out.print("enter your password again: ");
            String password2 = sc.next();
            if (password1.equals(password2)) {
                user.setPassword(password1);
                break;
            } else {
                System.out.println("The passwords you entered twice do not match. set again. ");
            }
        }


        // idCard
        while (true) {
            System.out.print("enter idCard: ");
            String idCard = sc.next();
            if (checkIdCard(idCard)) {
                user.setIdCard(idCard);
                break;
            } else {
                System.out.println("idCard illegal. enter again");
            }
        }

        // phone
        while (true) {
            System.out.print("enter phone: ");
            String phone = sc.next();
            if (checkPhone(phone)) {
                user.setPhone(phone);
                break;
            } else {
                System.out.println("phone illegal. enter again");
            }
        }

        users.add(user);

    }


    public static void forgetPassword(ArrayList<User> users) {
        Scanner sc = new Scanner(System.in);
        String name;
        int index = 0;
        // username
        while (true) {
            System.out.print("enter username:");
            name = sc.next();
            index = findUser(users, name);
            if (index != -1) {
                break;
            } else {
                System.out.println("username is not exist, register first. ");
                return ;
            }
        }

        System.out.print("enter idCard: ");
        String idCard = sc.next();
        System.out.print("enter phone: ");
        String phone = sc.next();

        User user = users.get(index);
        if (user.getIdCard().equals(idCard) && user.getPhone().equals(phone)) {
            System.out.print("enter new password: ");
            users.get(index).setPassword(sc.next());
        } else {
            System.out.println("wrong idCard or phone, change password failed. ");
        }
    }
}