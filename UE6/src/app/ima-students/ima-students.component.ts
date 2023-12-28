import {Component, OnInit} from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormControl, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HttpClient} from "@angular/common/http";
import {ActivatedRoute} from "@angular/router";

interface Student {
  name: string;
  image: string;
  studyProgram: string;
}

@Component({
  selector: 'app-ima-students',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './ima-students.component.html',
  styleUrl: './ima-students.component.scss'
})
export class ImaStudentsComponent implements OnInit {

  allStudents: Student[] = [];
  filteredStudents: Student[] = [];

  filterFormControl = new FormControl('');

  constructor(private httpClient: HttpClient, private route: ActivatedRoute) {
  }

  ngOnInit():void {
    this.httpClient.get<Student[]>('/assets/imaStudents.json')
      .subscribe(allStudents => {
        this.allStudents = allStudents;
        this.filter(this.filterFormControl.value)
        this.filterFormControl.valueChanges.subscribe(value => {
          this.filter(value)
        })
      })
  }

  private filter(filterValue: string | null) {
    this.filteredStudents = this.allStudents.filter(student => {
      return !filterValue || student.name.toLowerCase().includes(filterValue.toLowerCase()) ||
        student.studyProgram.toLowerCase().includes(filterValue.toLowerCase())
    })
  }
}
