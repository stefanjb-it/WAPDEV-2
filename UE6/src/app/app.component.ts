import {Component, OnInit} from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import {AlertButtonComponent} from "./alert-button/alert-button.component";
import {FhNewsComponent} from "./fh-news/fh-news.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, AlertButtonComponent, FhNewsComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  title = 'UE6';
  calculatedValue = 0;

  ngOnInit(): void {
    this.calculatedValue = this.add(1,1)
  }

  add(a: number, b: number): number {
    return a + b;
  }

  createDate(): string {
    return new Date().toLocaleDateString();
  }

  protected readonly Date = Date;
}
