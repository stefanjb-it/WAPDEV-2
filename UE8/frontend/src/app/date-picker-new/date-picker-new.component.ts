import {Component, forwardRef, Input, OnInit} from '@angular/core';
import {
  ControlValueAccessor,
  FormBuilder,
  FormControl,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule,
  Validators
} from "@angular/forms";
import {MatInputModule} from "@angular/material/input";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatNativeDateModule} from "@angular/material/core";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-date-picker-new',
  standalone: true,
  imports: [
    MatInputModule,
    MatDatepickerModule,
    ReactiveFormsModule,
    NgIf,
    MatNativeDateModule
  ],
  templateUrl: './date-picker-new.component.html',
  styleUrl: './date-picker-new.component.scss',
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => DatePickerNewComponent),
      multi: true
    }
  ]
})
export class DatePickerNewComponent implements OnInit, ControlValueAccessor{
  date: FormControl = new FormControl();
  private propagateChange: any;

  @Input()
  placeholder = '';
  @Input()
  title: string = 'Date';
  @Input()
  required = false;

  constructor(private fb: FormBuilder) {
  }

  ngOnInit() {
    let validator = null;
    if (this.required) {
      validator = Validators.required;
    }
    this.date = this.fb.control(null, {validators: validator});
    this.date.valueChanges.subscribe((newValue) => {
      const newDate = newValue ? new Date(newValue.getTime() - (newValue.getTimezoneOffset() * 60000)).toISOString().slice(0, 10) : null;
      this.propagateChange(newDate);
    });
  }

  registerOnChange(fn: any): void {
    this.propagateChange = fn;
  }

  registerOnTouched(fn: any): void {
    // do nothing
  }

  setDisabledState(isDisabled: boolean): void {
    // do nothing
  }

  writeValue(obj: any): void {
    this.date.patchValue(obj, {emitEvent: false});
  }

  hasError(errorName: string) {
    return this.date.hasError(errorName);
  }
}
