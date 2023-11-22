import {Component, Input} from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alert-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './alert-button.component.html',
  styleUrl: './alert-button.component.scss'
})
export class AlertButtonComponent {

  @Input() alertMessage = 'Alert';
  @Input() alertButtonText : string = 'New Alert!';

  showAlert() {
    alert(this.alertMessage);
  }
}
