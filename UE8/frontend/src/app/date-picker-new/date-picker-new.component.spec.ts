import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatePickerNewComponent } from './date-picker-new.component';

describe('DatePickerNewComponent', () => {
  let component: DatePickerNewComponent;
  let fixture: ComponentFixture<DatePickerNewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DatePickerNewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DatePickerNewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
