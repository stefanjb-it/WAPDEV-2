import {Component, forwardRef, Input, OnInit} from '@angular/core';
import {ControlValueAccessor, FormBuilder, FormControl, NG_VALUE_ACCESSOR, ReactiveFormsModule} from "@angular/forms";
import {MatSliderModule} from "@angular/material/slider";
import {MatInputModule} from "@angular/material/input";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-rating-slider',
  standalone: true,
  imports: [
    MatSliderModule,
    ReactiveFormsModule,
    MatInputModule,
    NgIf
  ],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: RatingSliderComponent,
      multi: true
    }
  ],
  templateUrl: './rating-slider.component.html',
  styleUrl: './rating-slider.component.scss'
})
export class RatingSliderComponent implements OnInit, ControlValueAccessor {
  @Input() label: string = "";
  @Input() placeholder: string = "placeholder";
  @Input() errors: any;
  textControl = new FormControl('');

  ngOnInit() {
  }

  onChange: any = () => {};
  onTouched: any = () => {};

  constructor() { }

  writeValue(value: any): void {
    //this.value = value;
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  setDisabledState?(isDisabled: boolean): void {
    if (isDisabled) {
      this.textControl.disable();
    } else {
      this.textControl.enable();
    }
  }

}
