#ifndef CODETAILSDIALOG_H
#define CODETAILSDIALOG_H

#include <QDialog>

namespace Ui {
class CODetailsDialog;
}

class CODetailsDialog : public QDialog
{
    Q_OBJECT
    
public:
    explicit CODetailsDialog(QWidget *parent = 0);
    ~CODetailsDialog();
    
protected:
    void changeEvent(QEvent *e);
    
private:
    Ui::CODetailsDialog *ui;
};

#endif // CODETAILSDIALOG_H
