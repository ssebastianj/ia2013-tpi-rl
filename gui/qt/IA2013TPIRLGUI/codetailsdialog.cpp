#include "codetailsdialog.h"
#include "ui_codetailsdialog.h"

CODetailsDialog::CODetailsDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::CODetailsDialog)
{
    ui->setupUi(this);
}

CODetailsDialog::~CODetailsDialog()
{
    delete ui;
}

void CODetailsDialog::changeEvent(QEvent *e)
{
    QDialog::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
}
