import {Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-fh-news',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './fh-news.component.html',
  styleUrl: './fh-news.component.scss'
})
export class FhNewsComponent {

  @Input() title: string | undefined;
  @Input() description: string | undefined;
  @Input() date: string | undefined;
  @Input() image: string | undefined;

}
