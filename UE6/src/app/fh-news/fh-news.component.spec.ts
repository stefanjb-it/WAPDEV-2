import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FhNewsComponent } from './fh-news.component';

describe('FhNewsComponent', () => {
  let component: FhNewsComponent;
  let fixture: ComponentFixture<FhNewsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FhNewsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FhNewsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
