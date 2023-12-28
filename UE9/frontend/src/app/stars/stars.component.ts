import {Component} from "@angular/core";
import {FormGroup, FormControl, ReactiveFormsModule} from "@angular/forms";
import {StarRatingModule} from "angular-star-rating";
import {json} from "express";

@Component({
  selector: 'app-stars',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    StarRatingModule
  ],
  template: `
    <form [formGroup]="form">
      <star-rating-control formControlName="myRatingControl"></star-rating-control>
      <!--<pre>{{ form.value | json }}</pre>-->
    </form>
  `
})
export class StarsComponent {

  form = new FormGroup({
    myRatingControl: new FormControl('')
  });

}
