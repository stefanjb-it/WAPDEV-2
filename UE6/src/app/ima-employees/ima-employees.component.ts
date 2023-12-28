import {Component, OnInit} from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import {FormControl, ReactiveFormsModule} from "@angular/forms";
import {ActivatedRoute} from "@angular/router";

interface Employee {
  name: string;
  image: string;
  position: string;
  description?: string;
}

@Component({
  selector: 'app-ima-employees',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './ima-employees.component.html',
  styleUrl: './ima-employees.component.scss'
})

export class ImaEmployeesComponent implements OnInit {

  allEmployees: Employee[] = [];
  filteredEmployees: Employee[] = [];
  positions: Set<string> = new Set();

  filterFormControl = new FormControl('');
  selectFormControl = new FormControl('');
  constructor(private httpClient: HttpClient, private route: ActivatedRoute) {
  }

  ngOnInit():void {
    this.httpClient.get<Employee[]>('/assets/imaEmployees.json')
      .subscribe(allEmployees => {
        this.allEmployees = allEmployees;
        this.filter(this.filterFormControl.value)
        this.filterFormControl.valueChanges.subscribe(value => {
          this.filter(value)
        })
        this.selectFormControl.valueChanges.subscribe(value => {
          this.filter(value)
        })
        this.positions = new Set(this.allEmployees.map(value => value.position));
      })
    this.route.paramMap.subscribe(value => {
      this.filter(value.get('filter'))
    })
  }

  private filter(filterValue: string | null) {
    this.filteredEmployees = this.allEmployees.filter(employee => {
      return !filterValue || employee.name.toLowerCase().includes(filterValue.toLowerCase()) ||
        employee.position.toLowerCase().includes(filterValue.toLowerCase());
    })
  }

  resetForms() {
    this.selectFormControl.reset()
    this.filterFormControl.reset()
  }
}
